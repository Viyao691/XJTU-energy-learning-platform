"""Check the live HTTPS data path with temporary server-prepared test sessions.

This does not prove mailbox delivery or email-code login, and calls no model.
"""
import json
import secrets
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import fitz
import httpx
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.auth import SESSION_COOKIE, _hash
from app.auth_models import WebSession, WebUser
from app.config import get_settings
from app.database import Base, make_engine
import app.models
import app.web_model_models

settings = get_settings()
engine = make_engine()
users = []
clients = []
paid_user = None
result = {"server_prepared_test_sessions": True, "real_email_login": False, "paid_generation": False}
try:
    for index in range(2):
        token, csrf = secrets.token_urlsafe(48), secrets.token_urlsafe(32)
        with Session(engine) as db:
            user = WebUser(email=f"deployment-smoke-{secrets.token_hex(8)}@example.invalid", verified_at=datetime.utcnow())
            db.add(user)
            db.flush()
            users.append(user.id)
            db.add(WebSession(user_id=user.id, token_hash=_hash(token), csrf_token=csrf, expires_at=datetime.utcnow() + timedelta(minutes=15)))
            db.commit()
        cookies = httpx.Cookies()
        cookies.set(SESSION_COOKIE, token, domain="energy.viyao.cn", path="/")
        clients.append(httpx.Client(base_url="https://energy.viyao.cn/backend-api", cookies=cookies, headers={"Origin": settings.web_origin, "X-CSRF-Token": csrf}, timeout=30))
    first, second = clients
    assert first.get("/api/v1/auth/me").status_code == 200
    document = fitz.open()
    document.new_page().insert_text((72, 72), "Synthetic deployment check. No measured scientific results.")
    pdf = document.tobytes()
    document.close()
    upload = first.post("/api/v1/papers/upload", files={"file": ("deployment-smoke.pdf", pdf, "application/pdf")})
    assert upload.status_code == 201, f"PDF upload status {upload.status_code}"
    paper_id = upload.json()["id"]
    task_id = upload.headers["X-Task-Id"]
    assert first.get(f"/api/v1/papers/{paper_id}/file").content == pdf
    assert first.put(f"/api/v1/papers/{paper_id}/note", json={"content": "runtime test note"}).status_code == 200
    assert second.get(f"/api/v1/papers/{paper_id}/file").status_code == 404
    assert second.get(f"/api/v1/tasks/{task_id}").status_code == 404
    assert second.put(f"/api/v1/papers/{paper_id}/note", json={"content": "overwrite"}).status_code == 404
    assert second.get("/api/v1/settings").status_code == 403
    assert second.get("/api/v1/papers").json()["items"] == []
    cache = first.get("/api/v1/papers").headers["cache-control"]
    assert "no-store" in cache and "public" not in cache, cache
    assert first.post(f"/api/v1/papers/{paper_id}/ocr-runs").status_code == 503
    if "--model" in sys.argv:
        paid_user = users[0]
        generated = first.post(f"/api/v1/papers/{paper_id}/analysis/quick_understanding", timeout=420)
        assert generated.status_code == 200, f"Model report status {generated.status_code}"
        report = generated.json()["quick_understanding"]
        assert isinstance(report, str) and len(report) > 100
        result.update(paid_generation=True, model_report_characters=len(report), evidence_status=generated.json()["evidence_status"])
    with tempfile.TemporaryDirectory() as directory:
        snapshot = Path(directory) / "snapshot.db"
        source = sqlite3.connect(f"file:{engine.url.database}?mode=ro", uri=True)
        restored = sqlite3.connect(snapshot)
        source.backup(restored)
        assert restored.execute("pragma integrity_check").fetchone()[0] == "ok"
        assert restored.execute("select content from notes where user_id=?", (users[0],)).fetchone()[0] == "runtime test note"
        restored.close()
        source.close()
        copied = Path(directory) / "paper.pdf"
        copied.write_bytes(first.get(f"/api/v1/papers/{paper_id}/file").content)
        assert copied.read_bytes() == pdf
    result.update(live_pdf_note_tenant_task_checks=True, sqlite_backup_restore_copy=True)
finally:
    for client in clients:
        client.close()
    # Remove only rows/files owned by the accounts created above; no billing rows.
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            if "user_id" in table.c and table.name != "web_model_calls":
                connection.execute(delete(table).where(table.c.user_id.in_(users)))
        # Preserve the billed test identity so later real users never reuse it.
        connection.execute(delete(WebUser).where(WebUser.id.in_([item for item in users if item != paid_user])))
    root = Path(settings.paper_storage_path).resolve()
    for user_id in users:
        directory = root / "users" / str(user_id)
        assert directory.resolve().is_relative_to(root)
        if directory.exists():
            shutil.rmtree(directory)
print(json.dumps(result))
