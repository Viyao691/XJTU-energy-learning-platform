from datetime import datetime, timedelta
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select

from test_web_auth import EMAIL, ORIGIN, PASSWORD, auth_api, login, register, send_code


def password_login(client, email=EMAIL, password=PASSWORD, **kwargs):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password}, **kwargs)


def test_registration_salts_password_and_password_login_rotates_session(auth_api):
    from app.auth_models import WebSession, WebUser
    client, factory, mail, _ = auth_api
    send_code(client)
    first = register(client, mail)
    assert first.status_code == 200
    second = password_login(client, "  READER@EXAMPLE.TEST ")
    assert second.status_code == 200, second.text
    assert second.json()["user"] == first.json()["user"]
    assert second.json()["csrf_token"] != first.json()["csrf_token"]
    assert PASSWORD not in second.text and "password_hash" not in second.text
    assert "Secure" in second.headers["set-cookie"] and "HttpOnly" in second.headers["set-cookie"]
    assert client.get("/api/v1/auth/me").json() == second.json()
    assert client.post("/private-write", headers={"X-CSRF-Token": second.json()["csrf_token"]}).status_code == 200
    assert client.post("/private-write").status_code == 403
    send_code(client, "second@example.test")
    assert register(client, mail, "second@example.test").status_code == 200
    with factory() as db:
        users = db.scalars(select(WebUser).order_by(WebUser.id)).all()
        assert users[0].password_hash != users[1].password_hash
        assert all(PASSWORD not in user.password_hash for user in users)
        assert db.scalar(select(WebSession).order_by(WebSession.id)).revoked_at is not None


def test_password_failure_is_uniform_and_does_equal_hash_work(auth_api, monkeypatch):
    from app import auth
    from app.auth_models import WebSession, WebUser
    client, factory, mail, _ = auth_api
    send_code(client)
    register(client, mail)
    with factory() as db:
        db.add(WebUser(email="legacy@example.test", verified_at=datetime.utcnow()))
        db.commit()
    calls = []
    derive = auth.hashlib.pbkdf2_hmac

    def tracked(*args, **kwargs):
        calls.append((args[0], args[3]))
        return derive(*args, **kwargs)

    monkeypatch.setattr(auth.hashlib, "pbkdf2_hmac", tracked)
    responses = [password_login(client, email, "incorrect password") for email in (EMAIL, "unknown@example.test", "legacy@example.test")]
    assert [r.status_code for r in responses] == [401, 401, 401]
    assert responses[0].json() == responses[1].json() == responses[2].json()
    assert all("set-cookie" not in r.headers for r in responses)
    assert len(calls) == 3 and calls == [("sha256", 600_000)] * 3
    with factory() as db:
        assert len(db.scalars(select(WebUser)).all()) == 2
        assert len(db.scalars(select(WebSession)).all()) == 1


def test_legacy_user_keeps_code_login_and_null_password(auth_api):
    from app.auth_models import WebUser
    client, factory, mail, _ = auth_api
    with factory() as db:
        db.add(WebUser(email=EMAIL, verified_at=datetime.utcnow()))
        db.commit()
    assert password_login(client).status_code == 401
    send_code(client)
    assert login(client, mail).status_code == 200
    with factory() as db:
        assert db.scalar(select(WebUser)).password_hash is None


@pytest.mark.parametrize("password", ["", "short", "x" * 129, None])
def test_registration_requires_valid_password(auth_api, password):
    client, factory, mail, _ = auth_api
    from app.auth_models import WebUser
    send_code(client)
    payload = {"email": EMAIL, "code": mail[-1][1]}
    if password is not None:
        payload["password"] = password
    assert client.post("/api/v1/auth/register", json=payload).status_code == 422
    with factory() as db:
        assert db.scalars(select(WebUser)).all() == []


@pytest.mark.parametrize("credentials", [{}, {"code": "123456", "password": PASSWORD}, {"password": None}, {"code": None, "password": PASSWORD}, {"password": "x" * 129}])
def test_login_rejects_missing_or_ambiguous_credentials(auth_api, credentials):
    client, _, _, _ = auth_api
    assert client.post("/api/v1/auth/login", json={"email": EMAIL, **credentials}).status_code == 422


def test_password_origin_desktop_mode_and_exact_password(auth_api):
    client, _, mail, settings = auth_api
    send_code(client)
    register(client, mail)
    assert password_login(client, headers={"Origin": ORIGIN + ".evil"}).status_code == 403
    assert password_login(client, password=" " + PASSWORD).status_code == 401
    assert password_login(client).status_code == 200
    settings.web_mode = False
    assert password_login(client).status_code == 404


def test_password_email_failures_persist_and_expire_without_blocking_code(auth_api):
    from app import auth
    from app.auth_models import WebPasswordFailure
    client, factory, mail, _ = auth_api
    send_code(client)
    register(client, mail)
    for _ in range(auth.PASSWORD_EMAIL_ATTEMPTS):
        assert password_login(client, password="incorrect password").status_code == 401
    # Every request uses a new DB session; the lockout is stored in SQLite.
    with factory() as db:
        assert len(db.scalars(select(WebPasswordFailure)).all()) == auth.PASSWORD_EMAIL_ATTEMPTS
    blocked = password_login(client)
    assert blocked.status_code == 429
    assert int(blocked.headers["Retry-After"]) > 0
    # Existing email-code fallback is independent of password lockout.
    from app.auth_models import WebEmailCode
    with factory() as db:
        db.scalar(select(WebEmailCode)).created_at -= timedelta(seconds=61)
        db.commit()
    send_code(client)
    assert login(client, mail).status_code == 200
    with factory() as db:
        for failure in db.scalars(select(WebPasswordFailure)):
            failure.created_at = datetime.utcnow() - timedelta(seconds=auth.PASSWORD_WINDOW_SECONDS + 1)
        db.commit()
    assert password_login(client).status_code == 200


def test_password_client_limit_prevents_spray_and_ignores_spoofed_proxy(auth_api, monkeypatch):
    from app import auth
    client, _, _, _ = auth_api
    monkeypatch.setattr(auth, "PASSWORD_CLIENT_ATTEMPTS", 2)
    for number in range(2):
        assert password_login(client, f"unknown{number}@example.test", headers={"X-Energy-Client-IP": f"198.51.100.{number + 1}"}).status_code == 401
    assert password_login(client, "unknown3@example.test").status_code == 429


def test_password_trusted_proxy_uses_validated_client_ip(auth_api, monkeypatch):
    from app import auth
    client, _, _, settings = auth_api
    settings.auth_trust_proxy = True
    monkeypatch.setattr(auth, "PASSWORD_CLIENT_ATTEMPTS", 1)
    assert password_login(client, "first@example.test", headers={"X-Energy-Client-IP": "198.51.100.1"}).status_code == 401
    assert password_login(client, "second@example.test", headers={"X-Energy-Client-IP": "198.51.100.1"}).status_code == 429
    assert password_login(client, "second@example.test", headers={"X-Energy-Client-IP": "198.51.100.2"}).status_code == 401


def test_password_migration_preserves_existing_users_and_sessions(tmp_path, monkeypatch):
    from alembic import command
    from alembic.config import Config
    from app.config import reset_settings_cache
    database = f"sqlite:///{tmp_path / 'migration.db'}"
    monkeypatch.setenv("DATABASE_URL", database)
    reset_settings_cache()
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    command.upgrade(config, "0032")
    engine = create_engine(database)
    try:
        with engine.begin() as db:
            db.exec_driver_sql("INSERT INTO web_users(id,email,created_at,verified_at) VALUES(1,'legacy@example.test',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)")
            db.exec_driver_sql("INSERT INTO web_sessions(user_id,token_hash,csrf_token,created_at,expires_at) VALUES(1,'keep-token','keep-csrf',CURRENT_TIMESTAMP,'2099-01-01')")
        command.upgrade(config, "head")
        with engine.connect() as db:
            assert db.exec_driver_sql("SELECT email,password_hash FROM web_users").one() == ("legacy@example.test", None)
            assert db.exec_driver_sql("SELECT token_hash,csrf_token FROM web_sessions").one() == ("keep-token", "keep-csrf")
            assert db.exec_driver_sql("SELECT version_num FROM alembic_version").scalar() == "0033"
            assert db.exec_driver_sql("SELECT COUNT(*) FROM web_password_failures").scalar() == 0
        command.downgrade(config, "0032")
        with engine.connect() as db:
            assert db.exec_driver_sql("SELECT email FROM web_users").scalar() == "legacy@example.test"
            assert db.exec_driver_sql("SELECT token_hash FROM web_sessions").scalar() == "keep-token"
    finally:
        engine.dispose()
        reset_settings_cache()
