from pathlib import Path

import fitz
import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient


@pytest.fixture()
def web_api(tmp_path, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    monkeypatch.setenv("WEB_ORIGIN", "https://energy.example.test")
    monkeypatch.setenv("AUTH_CODE_SECRET", "test-only-secret")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'web.db'}")
    monkeypatch.setenv("PAPER_STORAGE_PATH", str(tmp_path / "papers"))
    from app.config import reset_settings_cache
    reset_settings_cache()
    command.upgrade(Config(str(Path(__file__).resolve().parents[1] / "alembic.ini")), "head")
    from app import auth
    from app.main import create_app
    inbox = []
    monkeypatch.setattr(auth, "send_email_code", lambda email, code, settings: inbox.append((email, code)))
    api = create_app()
    with TestClient(api, base_url="https://energy.example.test", headers={"Origin": "https://energy.example.test"}) as client:
        yield client, inbox
    reset_settings_cache()


def log_in(client, inbox, email):
    client.cookies.clear()
    assert client.post("/api/v1/auth/email-code", json={"email": email, "intent": "register"}).status_code == 202
    response = client.post("/api/v1/auth/register", json={"email": email, "code": inbox[-1][1]})
    assert response.status_code == 200, response.text
    client.headers["X-CSRF-Token"] = response.json()["csrf_token"]


def test_web_private_pdf_tasks_and_admin_boundaries(web_api):
    client, inbox = web_api
    assert client.get("/health").status_code == 200
    assert client.get("/api/v1/papers").status_code == 401
    log_in(client, inbox, "first@example.test")
    document = fitz.open()
    document.new_page().insert_text((72, 72), "A real native PDF for isolated storage")
    pdf = document.tobytes()
    document.close()
    upload = client.post("/api/v1/papers/upload", files={"file": ("paper.pdf", pdf, "application/pdf")})
    assert upload.status_code == 201, upload.text
    first_id = upload.json()["id"]
    assert client.get(f"/api/v1/papers/{first_id}/file").content.startswith(b"%PDF-")
    assert client.get("/api/v1/settings").status_code == 403
    assert client.post(f"/api/v1/papers/{first_id}/ocr-runs").status_code == 503
    saved = client.put(f"/api/v1/papers/{first_id}/note", json={"content": "my private note"})
    assert saved.status_code == 200, saved.text
    log_in(client, inbox, "second@example.test")
    assert client.get(f"/api/v1/papers/{first_id}").status_code == 404
    assert client.get(f"/api/v1/papers/{first_id}/file").status_code == 404
    assert client.put(f"/api/v1/papers/{first_id}/note", json={"content": "overwrite"}).status_code == 404
    assert client.request("DELETE", f"/api/v1/papers/{first_id}", json={"confirmation_title": upload.json()["title"]}).status_code == 404
    assert client.get("/api/v1/papers").json()["items"] == []
    second = client.post("/api/v1/papers/upload", files={"file": ("same.pdf", pdf, "application/pdf")})
    assert second.status_code == 201, second.text
    assert second.json()["id"] != first_id
    assert client.get("/api/v1/papers").headers["cache-control"] == "private, no-store"
    client.headers.pop("X-CSRF-Token")
    assert client.delete(f"/api/v1/papers/{second.json()['id']}").status_code == 403


def test_web_refuses_mock_paid_generation(web_api):
    client, inbox = web_api
    log_in(client, inbox, "third@example.test")
    assert client.post("/api/v1/tasks", json={"task_name": "test_local"}).status_code == 403
    from app.providers import MockModelProvider, make_provider
    assert not isinstance(make_provider("mock", "", "", "mock", 60), MockModelProvider)
