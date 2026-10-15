import importlib.util
from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

ORIGIN = "https://energy.example.test"


@pytest.fixture()
def feedback_api(tmp_path, monkeypatch):
    from app import auth
    from app.database import Base
    from app.web_access import install_web_access

    engine = create_engine(f"sqlite:///{tmp_path / 'feedback.db'}", connect_args={"check_same_thread": False})
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    settings = SimpleNamespace(
        web_mode=True, web_origin=ORIGIN, auth_admin_email="admin@example.test", auth_trust_proxy=False,
        auth_smtp_host="smtp.test", auth_smtp_from="service@example.test", auth_smtp_port=587,
        auth_smtp_ssl=False, auth_smtp_starttls=True, auth_smtp_username="service",
        auth_smtp_password=SecretStr("test-smtp-secret"), web_model_concurrency=1, web_task_queue_limit=2,
    )
    monkeypatch.setattr(auth, "get_settings", lambda: settings)
    messages = []

    class SMTP:
        def __init__(self, *args, **kwargs): pass
        def __enter__(self): return self
        def __exit__(self, *args): pass
        def starttls(self, **kwargs): pass
        def login(self, *args): pass
        def send_message(self, message): messages.append(message)

    api = FastAPI()
    api.state.session_factory = factory

    def get_db():
        with factory() as db:
            yield db

    if importlib.util.find_spec("app.routers.feedback") is not None:
        from app.routers.feedback import register_feedback_routes
        from app import feedback
        monkeypatch.setattr(feedback, "get_settings", lambda: settings)
        monkeypatch.setattr(feedback.smtplib, "SMTP", SMTP)
        register_feedback_routes(api, get_db)
    install_web_access(api, settings, factory)
    Base.metadata.create_all(engine)
    with TestClient(api, base_url=ORIGIN, headers={"Origin": ORIGIN}) as client:
        yield client, factory, messages, settings
    engine.dispose()


def test_guest_feedback_is_saved_and_notified_without_exposing_admin(feedback_api):
    client, factory, messages, _ = feedback_api
    response = client.post("/api/v1/feedback", json={"message": "  需要改进检索  ", "contact": "  reader@example.test  "})
    assert response.status_code == 200
    from app.feedback_models import WebFeedback
    assert set(response.json()) == {"message"}
    assert "已保存" in response.json()["message"]
    assert "admin@example.test" not in response.text
    assert response.headers["cache-control"] == "private, no-store"
    assert messages[0]["To"] == "admin@example.test"
    assert "需要改进检索" in messages[0].get_content()
    with factory() as db:
        item = db.scalar(select(WebFeedback))
        assert (item.message, item.contact, item.user_id) == ("需要改进检索", "reader@example.test", None)
        assert len(item.client_hash) == 64 and item.client_hash != "testclient"
        assert item.notified_at is not None


@pytest.mark.parametrize("payload", [
    {"message": ""}, {"message": " \n\t "}, {"message": "a" * 1001},
    {"message": "good", "contact": "a" * 201}, {"message": "good", "user_id": 55},
])
def test_invalid_feedback_has_no_side_effect(feedback_api, payload):
    from app.feedback_models import WebFeedback
    client, factory, messages, _ = feedback_api
    assert client.post("/api/v1/feedback", json=payload).status_code == 422
    with factory() as db:
        assert db.scalars(select(WebFeedback)).all() == []
    assert messages == []


@pytest.mark.parametrize("origin", ["https://other.test", ""])
def test_feedback_requires_same_origin(feedback_api, origin):
    client, _, messages, _ = feedback_api
    assert client.post("/api/v1/feedback", json={"message": "hello"}, headers={"Origin": origin}).status_code == 403
    assert messages == []


@pytest.mark.parametrize("failure", ["missing", "transport"])
def test_notification_failure_preserves_feedback_as_pending(feedback_api, monkeypatch, failure):
    from app.feedback_models import WebFeedback
    from app import feedback
    client, factory, messages, settings = feedback_api
    if failure == "missing":
        settings.auth_smtp_host = ""
    else:
        def fail(*args, **kwargs):
            raise OSError("test-smtp-secret")
        monkeypatch.setattr(feedback.smtplib, "SMTP", fail)
    response = client.post("/api/v1/feedback", json={"message": "must persist"})
    assert response.status_code == 200
    assert "已保存" in response.json()["message"] and "延迟" in response.json()["message"]
    assert "test-smtp-secret" not in response.text
    assert messages == []
    with factory() as db:
        item = db.scalar(select(WebFeedback))
        assert item.message == "must persist" and item.notified_at is None


def test_persistent_feedback_limit_expires_after_one_hour(feedback_api):
    from app.feedback_models import WebFeedback
    client, factory, _, _ = feedback_api
    for _ in range(5):
        assert client.post("/api/v1/feedback", json={"message": "hello"}).status_code == 200
    response = client.post("/api/v1/feedback", json={"message": "too much"})
    assert response.status_code == 429 and response.headers["retry-after"] == "3600"
    with factory() as db:
        rows = db.scalars(select(WebFeedback)).all()
        assert len(rows) == 5
        rows[0].created_at = datetime.utcnow() - timedelta(hours=1, seconds=1)
        db.commit()
    assert client.post("/api/v1/feedback", json={"message": "after expiry"}).status_code == 200


def test_logged_user_feedback_and_no_feedback_read_api(feedback_api):
    from app.auth import SESSION_COOKIE, _hash
    from app.auth_models import WebUser, WebSession
    from app.feedback_models import WebFeedback
    client, factory, _, _ = feedback_api
    now = datetime.utcnow()
    with factory() as db:
        user = WebUser(email="reader@example.test", verified_at=now)
        db.add(user)
        db.flush()
        user_id = user.id
        db.add(WebSession(user_id=user_id, token_hash=_hash("test-token"), csrf_token="test-csrf", expires_at=now + timedelta(days=1)))
        db.commit()
    client.cookies.set(SESSION_COOKIE, "test-token")
    assert client.post("/api/v1/feedback", json={"message": "signed in"}).status_code == 200
    with factory() as db:
        assert db.scalar(select(WebFeedback)).user_id == user_id
    assert client.get("/api/v1/feedback").status_code == 405
    assert client.get("/api/v1/feedback/1").status_code == 404
    client.cookies.clear()
    assert client.get("/api/v1/feedback").status_code == 401


def test_feedback_migration_preserves_account_and_can_downgrade(tmp_path, monkeypatch):
    from pathlib import Path
    from alembic import command
    from alembic.config import Config
    from sqlalchemy import inspect, text
    from app.config import reset_settings_cache

    url = f"sqlite:///{tmp_path / 'migration.db'}"
    monkeypatch.setenv("DATABASE_URL", url)
    monkeypatch.setenv("ENERGY_WEB_MODE", "false")
    reset_settings_cache()
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    command.upgrade(config, "0033")
    engine = create_engine(url)
    try:
        with engine.begin() as db:
            db.execute(text("INSERT INTO web_users (id,email,created_at,verified_at) VALUES (1,'migration@example.test',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        command.upgrade(config, "0034")
        assert "web_feedback" in inspect(engine).get_table_names()
        with engine.connect() as db:
            assert db.execute(text("SELECT email FROM web_users WHERE id=1")).scalar() == "migration@example.test"
            assert db.execute(text("SELECT version_num FROM alembic_version")).scalar() == "0034"
            assert db.execute(text("PRAGMA foreign_key_check")).all() == []
        command.downgrade(config, "0033")
        assert "web_feedback" not in inspect(engine).get_table_names()
    finally:
        engine.dispose()
        reset_settings_cache()
