import asyncio
import json
from datetime import datetime
from pathlib import Path

import pytest
import httpx
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def scheduler_database(tmp_path, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "false")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'scheduler.db'}")
    monkeypatch.setenv("PAPER_STORAGE_PATH", str(tmp_path / "papers"))
    monkeypatch.setenv("BACKUP_PATH", str(tmp_path / "backups"))
    from app.config import get_settings, reset_settings_cache
    reset_settings_cache()
    command.upgrade(Config(str(Path(__file__).resolve().parents[1] / "alembic.ini")), "head")
    engine = create_engine(get_settings().database_url)
    yield engine
    engine.dispose()
    reset_settings_cache()


@pytest.mark.parametrize("web,research,campus,expected", [
    (False, False, False, {"research", "campus"}),
    (True, False, False, set()),
    (True, True, False, {"research"}),
    (True, False, True, {"campus"}),
])
def test_scheduler_startup_flags_preserve_desktop_and_default_web_off(
    scheduler_database, monkeypatch, web, research, campus, expected,
):
    monkeypatch.setenv("ENERGY_WEB_MODE", str(web))
    monkeypatch.setenv("WEB_RESEARCH_SCHEDULER_ENABLED", str(research))
    monkeypatch.setenv("WEB_CAMPUS_SCHEDULER_ENABLED", str(campus))
    from app.main import create_app
    app = create_app()
    started = set()

    async def research_start():
        started.add("research")

    async def campus_start():
        started.add("campus")

    monkeypatch.setattr(app.state.research_scheduler, "start", research_start)
    monkeypatch.setattr(app.state.campus_service, "start", campus_start)
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        assert started == expected


def test_web_due_scan_runs_real_service_in_each_owner_scope_without_ai(scheduler_database, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    from app.config import get_settings, reset_settings_cache
    from app.auth_models import WebUser
    from app.models import ResearchSubscription, ResearchRun, ResearchRecommendation, ResearchNotification
    from app.ownership import OwnedSession, current_user_id
    from app.services.research import ResearchService
    from app.services.research_scheduler import ResearchScheduler
    from test_phase4_research import _research_paper
    from app.web_model_models import WebModelCall
    reset_settings_cache()
    bare = sessionmaker(scheduler_database, expire_on_commit=False)
    owned = sessionmaker(scheduler_database, class_=OwnedSession, expire_on_commit=False)
    now = datetime(2026, 10, 16)
    with bare() as db:
        db.add_all([WebUser(id=owner, email=f"owner{owner}@example.test", verified_at=now) for owner in (1, 2)])
        db.add_all([ResearchSubscription(user_id=owner, name=f"owner{owner}", query=f"query{owner}",
                                       sources_json='["openalex"]', interval_hours=24, enabled=True,
                                       next_run_at=now) for owner in (0, 1, 2, 99)])
        db.commit()
    calls = []

    class Client:
        async def __aenter__(self):
            return self
        async def __aexit__(self, *_):
            pass

    class Source:
        name = "openalex"
        async def search(self, query, filters):
            calls.append((current_user_id.get(), query))
            return [_research_paper(external_id=query, title=query)]

    def reject_model(*_, **__):
        raise AssertionError("subscription discovery must not call paid models")

    monkeypatch.setattr("app.providers.make_provider", reject_model)
    service = ResearchService(session_factory=owned, paper_source_builder=lambda *_: [Source()],
                              paper_source_client_factory=Client, settings_provider=get_settings,
                              now_provider=lambda: now)
    scheduler = ResearchScheduler(session_factory=owned, research_service=service,
                                  now_provider=lambda: now, web_scan_session_factory=bare)

    async def exercise():
        assert current_user_id.get() is None
        runs = await scheduler.run_due_once()
        assert [run.user_id for run in runs] == [1, 2]
        assert current_user_id.get() is None
        assert await scheduler.run_due_once() == []
        token = current_user_id.set(1)
        try:
            with bare() as db:
                active = dict(db.execute(select(ResearchSubscription.user_id, ResearchSubscription.id)
                                         .where(ResearchSubscription.user_id.in_([1, 2]))).all())
            for item_id in active.values():
                await scheduler._locks[item_id].acquire()
            try:
                assert scheduler.diagnostic_status()["running_subscription_ids"] == [active[1]]
            finally:
                for item_id in active.values():
                    scheduler._locks[item_id].release()
            with owned() as db:
                other = db.scalar(select(ResearchSubscription.id).where(ResearchSubscription.user_id == 2))
                assert other is None
            with bare() as db:
                other_id = db.scalar(select(ResearchSubscription.id).where(ResearchSubscription.user_id == 2))
            with pytest.raises(ValueError, match="not found"):
                await scheduler.run_now(other_id)
            assert current_user_id.get() == 1
        finally:
            current_user_id.reset(token)

    asyncio.run(exercise())
    assert calls == [(1, "query1"), (2, "query2")]
    with bare() as db:
        for model in (ResearchRun, ResearchRecommendation, ResearchNotification):
            assert list(db.scalars(select(model.user_id).order_by(model.user_id))) == [1, 2]
        assert db.scalar(select(func.count()).select_from(WebModelCall)) == 0


def test_web_public_campus_discovery_does_not_create_model_provider(scheduler_database, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    monkeypatch.setenv("MODEL_PROVIDER", "deepseek")
    from app.config import reset_settings_cache
    from app.services import campus_analysis
    reset_settings_cache()

    def reject(*_, **__):
        raise AssertionError("public campus background analysis must remain rule based")

    monkeypatch.setattr(campus_analysis, "get_model_api_key", lambda *_: "test-key")
    monkeypatch.setattr(campus_analysis, "make_provider", reject)
    from app.ownership import OwnedSession
    from app.campus_models import CampusSource, CampusEvent
    from app.services.campus import CampusService
    from app.web_model_models import WebModelCall
    factory = sessionmaker(scheduler_database, class_=OwnedSession, autoflush=False)
    now = datetime(2026, 10, 16)
    with factory() as db:
        assert campus_analysis.configured_provider(db)[2] is None
        db.add(CampusSource(key="test", name="test", group="学院", url="https://wljsxy.xjtu.edu.cn/",
                            priority=100, enabled=True))
        db.commit()

    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        if request.url.path == "/":
            return httpx.Response(200, text='<a href="/info/1/1.htm">2026储能创新大赛</a>')
        return httpx.Response(200, text='<meta name="Article_PublishDate" content="2026-10-16"><div class="v_news_content"><p>报名截止：2026年10月18日</p></div>')

    async def exercise():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            service = CampusService(factory, client=client, delay=0, now=lambda: now)
            assert await service.run_due_once() == 1
            assert await service.run_due_once() == 0

    asyncio.run(exercise())
    with factory() as db:
        event = db.scalar(select(CampusEvent))
        assert event.category == "竞赛创新"
        analysis = json.loads(event.analysis_json)
        assert analysis["method"] == "rule"
        assert "规则整理" in analysis["unknowns"][0]
        assert db.scalar(select(func.count()).select_from(WebModelCall)) == 0


@pytest.mark.parametrize("enabled", [False, True])
def test_web_subscription_api_flag_auth_csrf_and_owner_isolation(scheduler_database, monkeypatch, enabled):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    monkeypatch.setenv("WEB_RESEARCH_SCHEDULER_ENABLED", str(enabled))
    monkeypatch.setenv("WEB_CAMPUS_SCHEDULER_ENABLED", "false")
    monkeypatch.setenv("AUTH_CODE_SECRET", "test-only-secret")
    monkeypatch.setenv("WEB_ORIGIN", "https://energy.example.test")
    from app import auth
    from app.main import create_app
    from test_web_integration import log_in
    inbox = []
    monkeypatch.setattr(auth, "send_email_code", lambda email, code, settings: inbox.append((email, code)))
    app = create_app()

    async def no_start():
        pass

    class Source:
        name = "openalex"
        async def search(self, *_):
            return []

    monkeypatch.setattr(app.state.research_scheduler, "start", no_start)
    app.state.paper_source_builder = lambda *_: [Source()]
    app.state.research_service._news_source_builder = None
    with TestClient(app, base_url="https://energy.example.test", headers={"Origin": "https://energy.example.test"}) as client:
        base = "/api/v1/research/subscriptions"
        assert client.get(base).status_code == 401
        log_in(client, inbox, "first@example.test")
        if not enabled:
            for method, path in [("GET", base), ("POST", base), ("GET", f"{base}/1"),
                                 ("PATCH", f"{base}/1"), ("DELETE", f"{base}/1"),
                                 ("POST", f"{base}/1/run"), ("GET", f"{base}/1/runs")]:
                assert client.request(method, path).status_code == 503
            return
        created = client.post(base, json={"name": "first subscription", "query": "storage", "sources": ["openalex"]})
        assert created.status_code == 201, created.text
        item = f"{base}/{created.json()['id']}"
        assert client.get(base).json()["total"] == 1
        assert client.patch(item, json={"name": "updated"}).status_code == 200
        csrf = client.headers.pop("X-CSRF-Token")
        assert client.post(item + "/run").status_code == 403
        client.headers["X-CSRF-Token"] = csrf
        run = client.post(item + "/run")
        assert run.status_code == 200, run.text
        assert "X-Task-Id" in run.headers
        assert client.get(item + "/runs").json()["total"] == 1
        log_in(client, inbox, "second@example.test")
        assert client.get(base).json()["total"] == 0
        for method, path, payload in [("GET", item, None), ("PATCH", item, {"name": "stolen"}),
                                      ("POST", item + "/run", None), ("GET", item + "/runs", None),
                                      ("DELETE", item, {"confirmation_name": "updated"})]:
            assert client.request(method, path, json=payload).status_code == 404
        assert client.get("/api/v1/research/runs").json()["total"] == 0
        assert client.get("/api/v1/research/recommendations").json()["total"] == 0
