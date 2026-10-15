"""Exercise the shipped Linux runtime with temporary data and fake mail only."""
import importlib.util
import json
import os
import sqlite3
import tempfile
from pathlib import Path

import fitz
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

with tempfile.TemporaryDirectory() as directory:
    os.environ.update(
        ENERGY_WEB_MODE="true", WEB_ORIGIN="https://energy.example.test",
        AUTH_CODE_SECRET="image-smoke-only", DATABASE_URL=f"sqlite:///{directory}/web.db",
        PAPER_STORAGE_PATH=f"{directory}/papers",
    )
    from app.config import reset_settings_cache
    reset_settings_cache()
    command.upgrade(Config("/app/alembic.ini"), "head")
    from app import auth
    from app.main import create_app
    inbox = []
    auth.send_email_code = lambda email, code, settings: inbox.append(code)
    with TestClient(create_app(), base_url="https://energy.example.test", headers={"Origin": "https://energy.example.test"}) as client:
        assert client.get("/health/ready").status_code == 200
        assert client.get("/api/v1/papers").status_code == 401

        def login(email):
            client.cookies.clear()
            assert client.post("/api/v1/auth/email-code", json={"email": email}).status_code == 202
            response = client.post("/api/v1/auth/register", json={"email": email, "code": inbox[-1]})
            assert response.status_code == 200, response.text
            client.headers["X-CSRF-Token"] = response.json()["csrf_token"]

        login("first@example.test")
        document = fitz.open()
        document.new_page().insert_text((72, 72), "Native PDF runtime smoke check")
        pdf = document.tobytes()
        document.close()
        upload = client.post("/api/v1/papers/upload", files={"file": ("smoke.pdf", pdf, "application/pdf")})
        assert upload.status_code == 201, upload.text
        paper_id = upload.json()["id"]
        assert upload.headers.get("X-Task-Id")
        assert client.get(f"/api/v1/papers/{paper_id}/file").content.startswith(b"%PDF-")
        assert client.put(f"/api/v1/papers/{paper_id}/note", json={"content": "private"}).status_code == 200
        login("second@example.test")
        assert client.get(f"/api/v1/papers/{paper_id}/file").status_code == 404
        assert client.get("/api/v1/papers").json()["items"] == []
        assert client.get("/api/v1/settings").status_code == 403
        assert client.post(f"/api/v1/papers/{paper_id}/ocr-runs").status_code == 503
    assert sqlite3.sqlite_version_info == (3, 54, 0)
    assert os.getuid() == 10001
    assert all(importlib.util.find_spec(name) is None for name in ("torch", "paddle", "docling", "whisper"))
    print(json.dumps({"runtime": "passed", "sqlite": sqlite3.sqlite_version, "uid": os.getuid(), "real_mail_and_models": False}))
