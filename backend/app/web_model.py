"""Single-worker model admission and durable conservative budgets, in UTC.

The administrator supplies a per-request cost ceiling. Unknown actual fees are
never released or presented as measured billing; failures retain the allocation.
"""
from contextlib import contextmanager
from datetime import datetime, UTC
from decimal import Decimal, ROUND_UP
from functools import lru_cache
import threading

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.database import make_engine
from app.ownership import current_user_id
from app.providers import ModelProviderError
from app.web_model_models import WebModelCall


class WebModelGate:
    def __init__(self, settings, session_factory):
        self.settings = settings
        self.session_factory = session_factory
        self.condition = threading.Condition(threading.RLock())
        self.active = 0
        self.users = set()
        self.pending = 0

    @contextmanager
    def slot(self, user_id):
        with self.condition:
            available = lambda: self.active < self.settings.web_model_concurrency and user_id not in self.users
            if not available():
                if self.pending >= self.settings.web_task_queue_limit:
                    raise ModelProviderError("模型服务繁忙，请稍后重试")
                self.pending += 1
                try:
                    ready = self.condition.wait_for(available, self.settings.web_model_queue_timeout_seconds)
                finally:
                    self.pending -= 1
                if not ready:
                    raise ModelProviderError("模型服务繁忙，请稍后重试")
            self.active += 1
            self.users.add(user_id)
        try:
            yield
        finally:
            with self.condition:
                self.active -= 1
                self.users.remove(user_id)
                self.condition.notify_all()

    def reserve(self, user_id, provider, method, amount):
        now = datetime.now(UTC).replace(tzinfo=None)
        with self.condition, self.session_factory() as db:
            for since, global_budget, user_budget in (
                (now.replace(hour=0, minute=0, second=0, microsecond=0), self.settings.daily_budget, self.settings.web_user_daily_budget_cny),
                (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0), self.settings.monthly_budget, self.settings.web_user_monthly_budget_cny),
            ):
                total = select(func.coalesce(func.sum(WebModelCall.reserved_cny), 0)).where(WebModelCall.created_at >= since)
                if Decimal(str(db.scalar(total))) + amount > Decimal(str(global_budget)):
                    raise ModelProviderError("平台模型预算不足，请联系管理员")
                if Decimal(str(db.scalar(total.where(WebModelCall.user_id == user_id)))) + amount > Decimal(str(user_budget)):
                    raise ModelProviderError("用户模型预算不足，请稍后重试")
            row = WebModelCall(user_id=user_id, provider=provider, method=method, state="running", reserved_cny=amount, created_at=now)
            db.add(row)
            db.commit()
            return row.id

    def finish(self, call_id, state):
        with self.condition, self.session_factory() as db:
            row = db.get(WebModelCall, call_id)
            row.state = state
            row.settled_cny = row.reserved_cny
            row.finished_at = datetime.now(UTC).replace(tzinfo=None)
            db.commit()

    def call(self, provider, method, args, kwargs):
        ceiling = self.settings.web_embedding_call_reserve_cny if getattr(provider, "_budget_embedding", False) else self.settings.web_model_call_reserve_cny
        if ceiling <= 0:
            raise ModelProviderError("管理员尚未配置单次费用预留上限，远端模型暂不可用")
        user_id = current_user_id.get()
        if user_id is None:
            raise ModelProviderError("模型调用需要已登录用户")
        # The legacy analyze() method generates three separate reports.
        count = 3 if method == "analyze" else 1
        amount = (Decimal(str(ceiling)) * count).quantize(Decimal("0.000001"), rounding=ROUND_UP)
        try:
            with self.slot(user_id):
                call_id = self.reserve(user_id, provider.name, method, amount)
                state = "failed_cost_unknown"
                try:
                    result = getattr(provider, method)(*args, **kwargs)
                    state = "completed_cost_unknown"
                    return result
                finally:
                    self.finish(call_id, state)
        except SQLAlchemyError as exc:
            raise ModelProviderError("模型预算记录暂不可用，请稍后重试") from exc


@lru_cache(maxsize=1)
def get_web_model_gate():
    # A bare server session is intentional: aggregate platform budget checks
    # must cover every user's allocation rather than an OwnedSession scope.
    return WebModelGate(get_settings(), sessionmaker(bind=make_engine(), expire_on_commit=False))


class WebModelProvider:
    def __init__(self, provider, gate):
        self._provider = provider
        self._gate = gate

    def __getattr__(self, name):
        value = getattr(self._provider, name)
        if not callable(value) or name in {"test_connection", "list_models"}:
            return value
        if name.startswith("_"):
            raise AttributeError(name)
        return lambda *args, **kwargs: self._gate.call(self._provider, name, args, kwargs)


def wrap_web_provider(provider):
    if provider.name == "unconfigured":
        return provider
    provider.web_no_retry = True
    return WebModelProvider(provider, get_web_model_gate())


class WebEmbeddingProvider(WebModelProvider):
    def embed(self, texts):
        from app.knowledge import EmbeddingProviderError

        if not texts:
            return []
        try:
            return self._gate.call(self._provider, "embed", (texts,), {})
        except ModelProviderError as exc:
            raise EmbeddingProviderError(str(exc)) from exc

    def test_connection(self):
        from app.knowledge import EmbeddingProviderError

        try:
            self.embed(["connection test"])
            return True, f"远端嵌入模型 {self.model_name} 已就绪"
        except EmbeddingProviderError as exc:
            return False, str(exc)


def wrap_web_embedding_provider(provider):
    provider._budget_embedding = True
    return WebEmbeddingProvider(provider, get_web_model_gate())
