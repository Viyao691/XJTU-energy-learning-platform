from __future__ import annotations

import importlib.util
from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

ORIGIN = "https://energy.example.test"
EMAIL = "reader@example.test"


@pytest.fixture()
def auth_api(tmp_path, monkeypatch):
    from app.database import Base

    engine = create_engine(f"sqlite:///{tmp_path / 'auth.db'}", connect_args={"check_same_thread": False})
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    settings = SimpleNamespace(
        web_mode=True, web_origin=ORIGIN, auth_admin_email="admin@example.test",
        auth_code_secret=SecretStr("test-only-code-hmac-key"),
        auth_code_ttl_seconds=600, auth_code_resend_seconds=60,
        auth_code_hourly_limit=10, auth_client_hourly_limit=30, auth_trust_proxy=False,
        auth_code_max_attempts=5, auth_session_days=7,
    )
    mail = []
    api = FastAPI()

    def get_db():
        with factory() as db:
            yield db

    if importlib.util.find_spec("app.routers.auth") is not None:
        from app import auth
        from app.routers.auth import register_auth_routes

        monkeypatch.setattr(auth, "get_settings", lambda: settings)
        monkeypatch.setattr(auth, "send_email_code", lambda email, code, _settings: mail.append((email, code)))
        register_auth_routes(api, get_db)

        @api.post("/private-write")
        def private_write(request: Request):
            user = auth.authenticate(request, factory)
            assert user is not None
            auth.require_csrf(request)
            return {"id": user.id}

    Base.metadata.create_all(engine)
    with TestClient(api, base_url=ORIGIN, headers={"Origin": ORIGIN}) as client:
        yield client, factory, mail, settings
    engine.dispose()


def send_code(client, email=EMAIL):
    return client.post("/api/v1/auth/email-code", json={"email": email})


def login(client, mail, email=EMAIL):
    return client.post("/api/v1/auth/login", json={"email": email, "code": mail[-1][1]})


def register(client, mail, email=EMAIL):
    return client.post("/api/v1/auth/register", json={"email": email, "code": mail[-1][1]})


def test_register_creates_verified_user_and_session(auth_api):
    from app.auth_models import WebEmailCode, WebSession, WebUser
    client, factory, mail, _ = auth_api
    assert client.post("/api/v1/auth/email-code", json={"email": "  Reader@Example.test ", "intent": "register"}).status_code == 202
    response = register(client, mail)
    assert response.status_code == 200
    assert response.json()["user"]["email"] == EMAIL
    assert client.get("/api/v1/auth/me").json() == response.json()
    assert "Secure" in response.headers["set-cookie"]
    assert "HttpOnly" in response.headers["set-cookie"]
    assert response.headers["cache-control"] == "private, no-store"
    with factory() as db:
        user = db.scalar(select(WebUser))
        assert user.verified_at is not None
        assert db.scalar(select(WebSession)).user_id == user.id
        assert db.scalar(select(WebEmailCode)).consumed_at is not None
    assert login(client, mail).status_code == 400


def test_login_unknown_email_requires_registration_without_creating_user(auth_api):
    from app.auth_models import WebSession, WebUser
    client, factory, mail, _ = auth_api
    assert send_code(client).status_code == 202
    response = login(client, mail)
    assert response.status_code == 400
    assert "请先注册" in response.json()["detail"]
    assert "set-cookie" not in response.headers
    with factory() as db:
        assert db.scalars(select(WebUser)).all() == []
        assert db.scalars(select(WebSession)).all() == []


def test_duplicate_registration_preserves_user_and_existing_session(auth_api):
    from app.auth_models import WebEmailCode, WebSession, WebUser
    client, factory, mail, settings = auth_api
    send_code(client)
    first = register(client, mail)
    assert first.status_code == 200
    with factory() as db:
        user = db.scalar(select(WebUser))
        original = (user.id, user.created_at, user.verified_at)
        db.scalar(select(WebEmailCode)).created_at -= timedelta(seconds=settings.auth_code_resend_seconds + 1)
        db.commit()
    assert send_code(client).status_code == 202
    response = register(client, mail)
    assert response.status_code == 409
    assert "请直接登录" in response.json()["detail"]
    assert client.get("/api/v1/auth/me").json() == first.json()
    with factory() as db:
        users = db.scalars(select(WebUser)).all()
        assert len(users) == 1
        assert (users[0].id, users[0].created_at, users[0].verified_at) == original
        assert len(db.scalars(select(WebSession)).all()) == 1
        assert db.scalar(select(WebSession)).revoked_at is None
    assert login(client, mail).status_code == 200
    assert client.get("/api/v1/auth/me").json()["user"]["id"] == original[0]


def test_explicit_email_code_intent_checks_account_before_sending(auth_api):
    from app.auth_models import WebEmailCode
    client, factory, mail, settings = auth_api
    response = client.post("/api/v1/auth/email-code", json={"email": EMAIL, "intent": "login"})
    assert response.status_code == 400
    assert "请先注册" in response.json()["detail"]
    assert mail == []
    with factory() as db:
        assert db.scalars(select(WebEmailCode)).all() == []
    assert client.post("/api/v1/auth/email-code", json={"email": EMAIL, "intent": "register"}).status_code == 202
    assert register(client, mail).status_code == 200
    response = client.post("/api/v1/auth/email-code", json={"email": EMAIL, "intent": "register"})
    assert response.status_code == 409
    assert "请直接登录" in response.json()["detail"]
    assert len(mail) == 1
    with factory() as db:
        db.scalar(select(WebEmailCode)).created_at -= timedelta(seconds=settings.auth_code_resend_seconds + 1)
        db.commit()
    assert client.post("/api/v1/auth/email-code", json={"email": EMAIL, "intent": "login"}).status_code == 202
    assert login(client, mail).status_code == 200


def test_send_code_does_not_create_unverified_user(auth_api):
    client, factory, mail, _ = auth_api
    response = send_code(client, "  Reader@Example.test ")
    assert response.status_code == 202
    assert mail[0][0] == EMAIL
    assert mail[0][1] not in response.text
    from app.auth_models import WebEmailCode, WebUser
    with factory() as db:
        assert db.scalars(select(WebUser)).all() == []
        stored = db.scalar(select(WebEmailCode))
        assert stored.code_hash != mail[0][1]
        assert mail[0][1] not in stored.code_hash


def test_login_me_and_logout_secure_cookie(auth_api):
    from app.auth import SESSION_COOKIE
    from app.auth_models import WebSession, WebUser
    client, factory, mail, _ = auth_api
    assert client.get("/api/v1/auth/me").status_code == 401
    with factory() as db:
        db.add(WebUser(email=EMAIL, verified_at=datetime.utcnow()))
        db.commit()
    send_code(client)
    response = login(client, mail)
    assert response.status_code == 200
    body = response.json()
    assert body["user"]["email"] == EMAIL
    assert body["user"]["is_admin"] is False
    assert body["csrf_token"]
    cookie = response.headers["set-cookie"]
    assert cookie.startswith(f"{SESSION_COOKIE}=")
    assert "HttpOnly" in cookie and "Secure" in cookie and "SameSite=lax" in cookie
    assert "Path=/" in cookie and "Domain=" not in cookie
    raw_token = client.cookies.get(SESSION_COOKIE)
    with factory() as db:
        assert db.scalar(select(WebSession)).token_hash != raw_token
    assert client.get("/api/v1/auth/me").json() == body
    assert login(client, mail).status_code == 400
    assert client.post("/api/v1/auth/logout").status_code == 403
    assert client.post("/api/v1/auth/logout", headers={"X-CSRF-Token": body["csrf_token"]}).status_code == 200
    assert client.get("/api/v1/auth/me").status_code == 401
    client.cookies.set(SESSION_COOKIE, raw_token)
    assert client.get("/api/v1/auth/me").status_code == 401


def test_expiry_and_attempt_limit_never_create_user(auth_api):
    from app.auth_models import WebEmailCode, WebUser
    client, factory, mail, settings = auth_api
    send_code(client)
    with factory() as db:
        db.scalar(select(WebEmailCode)).expires_at = datetime.utcnow() - timedelta(seconds=1)
        db.commit()
    assert register(client, mail).status_code == 400
    send_code(client, "other@example.test")
    correct = mail[-1][1]
    wrong = "000000" if correct != "000000" else "111111"
    for _ in range(settings.auth_code_max_attempts):
        assert client.post("/api/v1/auth/register", json={"email": "other@example.test", "code": wrong}).status_code == 400
    assert register(client, mail, "other@example.test").status_code == 400
    with factory() as db:
        assert db.scalars(select(WebUser)).all() == []


def test_email_and_client_rate_limits(auth_api):
    client, _, mail, settings = auth_api
    assert send_code(client).status_code == 202
    assert send_code(client).status_code == 429
    assert len(mail) == 1
    settings.auth_client_hourly_limit = 2
    assert send_code(client, "other@example.test").status_code == 202
    assert send_code(client, "third@example.test").status_code == 429


def test_admin_and_session_expiry(auth_api):
    from app.auth_models import WebSession
    client, factory, mail, _ = auth_api
    send_code(client, "ADMIN@example.test")
    assert register(client, mail, "admin@example.test").json()["user"]["is_admin"] is True
    with factory() as db:
        db.scalar(select(WebSession)).expires_at = datetime.utcnow() - timedelta(seconds=1)
        db.commit()
    assert client.get("/api/v1/auth/me").status_code == 401


@pytest.mark.parametrize("email", ["", "bad", "x@y", "a b@example.test", "a@localhost", "a@example..test", "a\r\n@example.test"])
def test_invalid_email_rejected(auth_api, email):
    client, _, mail, _ = auth_api
    assert send_code(client, email).status_code == 422
    assert mail == []


def test_exact_origin_and_csrf_for_mutations(auth_api):
    client, _, mail, _ = auth_api
    assert send_code(client).status_code == 202
    assert client.post("/api/v1/auth/login", json={"email": EMAIL, "code": mail[-1][1]}, headers={"Origin": "https://evil.example.test"}).status_code == 403
    assert client.post("/api/v1/auth/register", json={"email": EMAIL, "code": mail[-1][1]}, headers={"Origin": "https://evil.example.test"}).status_code == 403
    token = register(client, mail).json()["csrf_token"]
    assert client.post("/private-write", headers={"X-CSRF-Token": token}).status_code == 200
    assert client.post("/private-write").status_code == 403
    assert client.post("/private-write", headers={"X-CSRF-Token": "incorrect"}).status_code == 403
    assert client.post("/private-write", headers={"Origin": ORIGIN + ".evil", "X-CSRF-Token": token}).status_code == 403
    client.headers.pop("origin")
    assert client.post("/private-write", headers={"X-CSRF-Token": token}).status_code == 403
    assert send_code(client, "new@example.test").status_code == 403


def test_sender_failure_no_code_or_secret_response(auth_api, monkeypatch):
    from app import auth
    from app.auth_models import WebEmailCode
    client, factory, _, _ = auth_api
    def fail_send(*_):
        raise RuntimeError("private SMTP password")
    monkeypatch.setattr(auth, "send_email_code", fail_send)
    response = send_code(client)
    assert response.status_code == 503
    assert "private SMTP" not in response.text
    with factory() as db:
        assert db.scalar(select(WebEmailCode)).consumed_at is not None


def test_desktop_auth_routes_disabled(auth_api):
    client, _, mail, settings = auth_api
    settings.web_mode = False
    assert send_code(client).status_code == 404
    assert client.get("/api/v1/auth/me").status_code == 404
    assert client.post("/api/v1/auth/register", json={"email": EMAIL, "code": "123456"}).status_code == 404
    assert mail == []


def test_non_ascii_csrf_header_rejected_without_server_error(auth_api):
    client, _, mail, _ = auth_api
    send_code(client)
    register(client, mail)
    assert client.post("/private-write", headers={"X-CSRF-Token": "invalid-é".encode("utf-8")}).status_code == 403


def test_auth_migration_round_trip(tmp_path):
    from pathlib import Path
    from alembic.migration import MigrationContext
    from alembic.operations import Operations
    from sqlalchemy import inspect

    path = Path(__file__).parents[1] / "alembic" / "versions" / "0030_web_auth.py"
    spec = importlib.util.spec_from_file_location("web_auth_migration", path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    engine = create_engine(f"sqlite:///{tmp_path / 'migration.db'}")
    with engine.begin() as connection:
        with Operations.context(MigrationContext.configure(connection)):
            migration.upgrade()
            assert set(inspect(connection).get_table_names()) == {"web_users", "web_email_codes", "web_sessions"}
            assert inspect(connection).get_foreign_keys("web_sessions")[0]["referred_table"] == "web_users"
            migration.downgrade()
            assert inspect(connection).get_table_names() == []
    engine.dispose()


def test_proxy_header_ignored_by_default(auth_api):
    client, _, _, settings = auth_api
    settings.auth_client_hourly_limit = 1
    assert client.post("/api/v1/auth/email-code", json={"email": EMAIL}, headers={"X-Energy-Client-IP": "198.51.100.1"}).status_code == 202
    assert client.post("/api/v1/auth/email-code", json={"email": "second@example.test"}, headers={"X-Energy-Client-IP": "198.51.100.2", "X-Forwarded-For": "198.51.100.3"}).status_code == 429


@pytest.mark.parametrize("first, equivalent, second", [
    ("198.51.100.1", "198.51.100.1", "198.51.100.2"),
    ("2001:db8::1", "2001:0db8:0:0:0:0:0:1", "2001:db8::2"),
])
def test_trusted_proxy_valid_ips_have_separate_limits(auth_api, first, equivalent, second):
    client, _, _, settings = auth_api
    settings.auth_trust_proxy = True
    settings.auth_client_hourly_limit = 1
    assert client.post("/api/v1/auth/email-code", json={"email": EMAIL}, headers={"X-Energy-Client-IP": first}).status_code == 202
    assert client.post("/api/v1/auth/email-code", json={"email": "second@example.test"}, headers={"X-Energy-Client-IP": second}).status_code == 202
    response = client.post("/api/v1/auth/email-code", json={"email": "third@example.test"}, headers={"X-Energy-Client-IP": equivalent, "X-Forwarded-For": "198.51.100.99"})
    assert response.status_code == 429
    assert response.headers["Retry-After"] == str(settings.auth_code_resend_seconds)


def test_trusted_proxy_invalid_ip_falls_back_to_peer(auth_api):
    client, _, _, settings = auth_api
    settings.auth_trust_proxy = True
    settings.auth_client_hourly_limit = 1
    assert client.post("/api/v1/auth/email-code", json={"email": EMAIL}, headers={"X-Energy-Client-IP": "198.51.100.1, 198.51.100.2"}).status_code == 202
    assert client.post("/api/v1/auth/email-code", json={"email": "second@example.test"}, headers={"X-Forwarded-For": "198.51.100.3"}).status_code == 429
