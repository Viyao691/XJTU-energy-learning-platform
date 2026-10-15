from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, UTC
from decimal import Decimal
import threading

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.config import AppSettings
from app.ownership import current_user_id
from app.providers import ModelProviderError


def setup_gate(tmp_path, **values):
    from app.web_model import WebModelGate
    from app.web_model_models import WebModelCall

    aliases = {"daily_budget": "DAILY_BUDGET_CNY", "monthly_budget": "MONTHLY_BUDGET_CNY"}
    settings = AppSettings(_env_file=None, web_mode=True, web_model_call_reserve_cny=0.5, **{aliases.get(key, key): value for key, value in values.items()})
    engine = create_engine(f"sqlite:///{tmp_path / 'budget.sqlite'}", connect_args={"check_same_thread": False})
    WebModelCall.__table__.create(engine)
    factory = sessionmaker(engine)
    return WebModelGate(settings, factory), factory


class FakeProvider:
    name = "fake"
    model_name = "fake-model"
    supports_vision = False

    def __init__(self):
        self.calls = []

    def generate_structured_task(self, prompt, task_type, *, max_tokens=None):
        self.calls.append((prompt, task_type, max_tokens))
        return {"answer": "ok"}


def call(gate, provider, user_id=1):
    from app.web_model import WebModelProvider

    token = current_user_id.set(user_id)
    try:
        return WebModelProvider(provider, gate).generate_structured_task("prompt", "test", max_tokens=64000)
    finally:
        current_user_id.reset(token)


def test_reservation_is_persisted_before_call_and_cost_stays_unknown(tmp_path):
    from app.web_model_models import WebModelCall

    gate, factory = setup_gate(tmp_path)
    provider = FakeProvider()
    original = provider.generate_structured_task

    def inspect_reservation(*args, **kwargs):
        with factory() as db:
            row = db.scalar(select(WebModelCall))
            assert row.state == "running"
            assert row.reserved_cny == Decimal("0.5")
            assert row.actual_cost_cny is None
        return original(*args, **kwargs)

    provider.generate_structured_task = inspect_reservation
    assert call(gate, provider) == {"answer": "ok"}
    assert provider.calls == [("prompt", "test", 64000)]
    with factory() as db:
        row = db.scalar(select(WebModelCall))
        assert row.state == "completed_cost_unknown"
        assert row.settled_cny == row.reserved_cny
        assert row.actual_cost_cny is None


def test_user_and_platform_budgets_block_before_paid_call(tmp_path):
    gate, _ = setup_gate(tmp_path, web_user_daily_budget_cny=0.5, daily_budget=1)
    provider = FakeProvider()
    call(gate, provider, 1)
    with pytest.raises(ModelProviderError, match="用户.*预算"):
        call(gate, provider, 1)
    call(gate, provider, 2)
    with pytest.raises(ModelProviderError, match="平台.*预算"):
        call(gate, provider, 3)
    assert len(provider.calls) == 2


def test_monthly_budget_counts_earlier_days(tmp_path):
    from app.web_model_models import WebModelCall

    gate, factory = setup_gate(tmp_path, monthly_budget=0.5)
    with factory() as db:
        db.add(WebModelCall(user_id=1, provider="fake", method="test", state="failed_cost_unknown", reserved_cny=0.5, settled_cny=0.5, created_at=datetime.now(UTC).replace(tzinfo=None, day=1, hour=0)))
        db.commit()
    provider = FakeProvider()
    with pytest.raises(ModelProviderError, match="平台.*预算"):
        call(gate, provider, 2)
    assert provider.calls == []


def test_failed_call_keeps_reservation_and_is_never_retried(tmp_path):
    from app.web_model_models import WebModelCall

    gate, factory = setup_gate(tmp_path)
    provider = FakeProvider()

    def fail(*args, **kwargs):
        provider.calls.append("failed")
        raise ModelProviderError("fake error")

    provider.generate_structured_task = fail
    with pytest.raises(ModelProviderError, match="fake error"):
        call(gate, provider)
    assert provider.calls == ["failed"]
    with factory() as db:
        row = db.scalar(select(WebModelCall))
        assert row.state == "failed_cost_unknown"
        assert row.settled_cny == Decimal("0.5")


def test_unconfigured_ceiling_and_missing_user_do_not_call_provider(tmp_path):
    gate, _ = setup_gate(tmp_path)
    gate.settings.web_model_call_reserve_cny = 0
    provider = FakeProvider()
    with pytest.raises(ModelProviderError, match="单次费用"):
        call(gate, provider)
    gate.settings.web_model_call_reserve_cny = 0.5
    with pytest.raises(ModelProviderError, match="登录"):
        call(gate, provider, None)
    assert provider.calls == []


def test_global_and_user_concurrency_are_bounded(tmp_path):
    gate, _ = setup_gate(tmp_path, web_model_concurrency=2, web_task_queue_limit=1, web_model_queue_timeout_seconds=0.1)
    started = threading.Event()
    release = threading.Event()
    provider = FakeProvider()

    def block(*args, **kwargs):
        started.set()
        release.wait(3)
        return "ok"

    provider.generate_structured_task = block
    with ThreadPoolExecutor(3) as pool:
        first = pool.submit(call, gate, provider, 1)
        assert started.wait(1)
        with pytest.raises(ModelProviderError, match="繁忙"):
            call(gate, provider, 1)
        started.clear()
        second = pool.submit(call, gate, provider, 2)
        assert started.wait(1)
        with pytest.raises(ModelProviderError, match="繁忙"):
            call(gate, provider, 3)
        release.set()
        assert first.result() == second.result() == "ok"


def test_factory_wraps_only_configured_web_cloud(monkeypatch, tmp_path):
    import app.config as config
    import app.web_model as web_model
    from app.providers import make_provider

    gate, _ = setup_gate(tmp_path)
    monkeypatch.setattr(config, "get_settings", lambda: gate.settings)
    monkeypatch.setattr(web_model, "get_web_model_gate", lambda: gate)
    assert isinstance(make_provider("openai_compatible", "fake-key", "https://model.test", "model", 30), web_model.WebModelProvider)
    assert make_provider("mock", "", "", "", 30).name == "unconfigured"
    assert make_provider("openai_compatible", "", "", "", 30).name == "unconfigured"


def test_web_embedding_uses_same_budget_with_separate_ceiling(tmp_path, monkeypatch):
    import app.web_model as web_model
    from app.knowledge import EmbeddingProviderError

    gate, factory = setup_gate(tmp_path)
    monkeypatch.setattr(web_model, "get_web_model_gate", lambda: gate)
    provider = FakeProvider()
    provider.embed = lambda texts: [[1, 0] for _ in texts]
    guarded = web_model.wrap_web_embedding_provider(provider)
    token = current_user_id.set(1)
    try:
        with pytest.raises(EmbeddingProviderError, match="单次费用"):
            guarded.embed(["text"])
        gate.settings.web_embedding_call_reserve_cny = 0.1
        assert guarded.embed(["text"]) == [[1, 0]]
        assert guarded.test_connection()[0] is True
    finally:
        current_user_id.reset(token)
    with factory() as db:
        records = db.scalars(select(web_model.WebModelCall)).all()
        assert len(records) == 2
        assert sum(row.reserved_cny for row in records) == Decimal("0.2")


def test_web_paid_visual_call_does_not_retry_for_language(tmp_path, monkeypatch):
    import httpx
    import app.providers as providers
    import app.web_model as web_model

    gate, _ = setup_gate(tmp_path)
    monkeypatch.setattr(web_model, "get_web_model_gate", lambda: gate)
    captured = []

    def fake_post(url, **kwargs):
        captured.append(kwargs)
        return httpx.Response(200, request=httpx.Request("POST", url), json={
            "choices": [{"message": {"content": "The diagram shows a battery mechanism and structural change. " * 30}}],
        })

    monkeypatch.setattr(providers.httpx, "post", fake_post)
    provider = web_model.wrap_web_provider(providers.DeepSeekProvider("fake-key", "https://fake.test/v1", "vision-model", 30))
    token = current_user_id.set(1)
    try:
        provider.analyze_visual("title", "caption", "page", b"fake-image")
    finally:
        current_user_id.reset(token)
    assert len(captured) == 1


@pytest.mark.parametrize("max_tokens", [None, 64000])
def test_web_deepseek_text_keeps_explicit_64k_budget(monkeypatch, max_tokens):
    import httpx
    import app.providers as providers

    calls = []

    def fake_post(url, **kwargs):
        calls.append(kwargs)
        return httpx.Response(200, request=httpx.Request("POST", url), json={
            "choices": [{"message": {"content": "ok"}, "finish_reason": "stop"}],
        })

    monkeypatch.setattr(providers.httpx, "post", fake_post)
    provider = providers.DeepSeekProvider("fake-key", "https://api.deepseek.com", "deepseek-v4-pro", 30)
    provider.web_no_retry = True
    assert provider._chat_content("prompt", max_tokens=max_tokens) == "ok"
    assert calls[0]["json"]["max_tokens"] == 64000
    assert "thinking" not in calls[0]["json"]


def test_web_deepseek_rejects_excess_input_or_output_before_network(monkeypatch):
    import app.providers as providers

    def unexpected(*args, **kwargs):
        pytest.fail("rejected request must not reach the network")

    monkeypatch.setattr(providers.httpx, "post", unexpected)
    provider = providers.DeepSeekProvider("fake-key", "https://api.deepseek.com", "deepseek-v4-pro", 30)
    provider.web_no_retry = True
    with pytest.raises(ModelProviderError, match="128000"):
        provider._chat_content("研" * 42667, max_tokens=64000)
    with pytest.raises(ModelProviderError, match="64000"):
        provider._chat_content("prompt", max_tokens=64001)
