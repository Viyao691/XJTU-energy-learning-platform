from datetime import datetime, timedelta
import json

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def reindex_api(tmp_path, monkeypatch):
    from app import auth, config, knowledge, ownership, web_model
    from app.auth_models import WebUser, WebSession
    from app.config import AppSettings
    from app.database import Base
    from app.ownership import OwnedSession
    from app.routers import knowledge as routes
    from app.web_access import install_web_access

    origin = "https://energy.example.test"
    settings = AppSettings(_env_file=None, web_mode=True, web_origin=origin,
                           embedding_provider="openai_compatible", embedding_model="fake-semantic",
                           embedding_base_url="https://embedding.test/v1", embedding_api_key="fake-key",
                           web_embedding_call_reserve_cny=0.001)
    for module in (auth, config, ownership, routes):
        monkeypatch.setattr(module, "get_settings", lambda: settings)
    engine = create_engine(f"sqlite:///{tmp_path / 'reindex.db'}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, class_=OwnedSession, expire_on_commit=False)
    raw_factory = sessionmaker(bind=engine, expire_on_commit=False)
    gate = web_model.WebModelGate(settings, raw_factory)
    monkeypatch.setattr(web_model, "get_web_model_gate", lambda: gate)
    requests = []

    def embed(request):
        body = json.loads(request.content)
        requests.append(body)
        return httpx.Response(200, json={"data": [
            {"index": index, "embedding": [1, 0]} for index in range(len(body["input"]))
        ]})

    remote = httpx.Client(transport=httpx.MockTransport(embed))
    monkeypatch.setattr(knowledge, "_remote_embedding_client", lambda: remote)
    with raw_factory() as db:
        for owner in (1, 2):
            db.add(WebUser(id=owner, email=f"reader{owner}@example.test", verified_at=datetime.utcnow()))
            db.add(WebSession(user_id=owner, token_hash=auth._hash(f"token{owner}"), csrf_token=f"csrf{owner}", expires_at=datetime.utcnow() + timedelta(days=1)))
        db.commit()
    api = FastAPI()
    api.state.session_factory = factory

    def get_db():
        with factory() as db:
            yield db

    routes.register_knowledge_routes(api, get_db)
    install_web_access(api, settings, raw_factory)
    with TestClient(api, base_url=origin, headers={"Origin": origin, "X-CSRF-Token": "csrf1"}) as client:
        client.cookies.set(auth.SESSION_COOKIE, "token1")
        yield client, factory, settings, requests
    remote.close()
    engine.dispose()


def seed_papers(factory, owner, count, *, content=True):
    from app.models import Paper
    with factory(user_id=owner) as db:
        items = [Paper(title=f"owner{owner}-{index}", abstract=f"sodium battery evidence {index}" if content else "", file_size=0) for index in range(count)]
        db.add_all(items)
        db.commit()
        return [item.id for item in items]


def test_web_reindex_batches_private_stale_papers_and_skips_current(reindex_api):
    from app.models import Paper, PaperChunk, TaskRun
    client, factory, _, requests = reindex_api
    mine = seed_papers(factory, 1, 7)
    other = seed_papers(factory, 2, 3)
    response = client.post("/api/v1/knowledge/reindex")
    assert response.status_code == 200, response.text
    assert response.json()["indexed_papers"] == 5
    assert response.headers["X-Task-Id"]
    with factory(user_id=1) as db:
        assert set(db.scalars(select(PaperChunk.paper_id))) == set(mine[:5])
        original_chunk_ids = list(db.scalars(select(PaperChunk.id).order_by(PaperChunk.id)))
        assert db.scalar(select(TaskRun).where(TaskRun.id == int(response.headers["X-Task-Id"]))).status == "completed"
    with factory(user_id=2) as db:
        assert db.scalars(select(PaperChunk)).all() == []
        assert set(db.scalars(select(Paper.id))) == set(other)
    status = client.get("/api/v1/knowledge/status").json()
    assert status["stale_papers"] == 2 and "5" in status["message"]
    assert client.post("/api/v1/knowledge/reindex").json()["indexed_papers"] == 2
    count_before = len(requests)
    assert client.post("/api/v1/knowledge/reindex").json()["indexed_papers"] == 0
    assert len(requests) == count_before  # No probe or charge when already current.
    with factory(user_id=1) as db:
        assert set(original_chunk_ids).issubset(set(db.scalars(select(PaperChunk.id))))
        db.get(Paper, mine[0]).knowledge_index_stale = True
        db.commit()
    assert client.post("/api/v1/knowledge/reindex").json()["indexed_papers"] == 1


def test_model_change_marks_existing_chunks_for_next_batch(reindex_api):
    client, factory, settings, _ = reindex_api
    seed_papers(factory, 1, 1)
    assert client.post("/api/v1/knowledge/reindex").json()["indexed_papers"] == 1
    settings.embedding_model = "replacement-semantic"
    assert client.get("/api/v1/knowledge/status").json()["stale_papers"] == 1
    assert client.post("/api/v1/knowledge/reindex").json()["indexed_papers"] == 1


def test_metadata_only_rows_do_not_block_later_indexable_papers(reindex_api):
    client, factory, _, _ = reindex_api
    seed_papers(factory, 1, 6, content=False)
    seed_papers(factory, 1, 1)
    assert client.post("/api/v1/knowledge/reindex").json()["indexed_papers"] == 1


def test_reindex_keeps_auth_csrf_and_model_budget_gate(reindex_api):
    client, factory, settings, requests = reindex_api
    seed_papers(factory, 1, 1)
    assert client.post("/api/v1/knowledge/reindex", headers={"X-CSRF-Token": "wrong"}).status_code == 403
    settings.web_embedding_call_reserve_cny = 0
    response = client.post("/api/v1/knowledge/reindex")
    assert response.status_code == 503 and "费用预留" in response.json()["detail"]
    assert requests == []
    client.cookies.clear()
    assert client.post("/api/v1/knowledge/reindex").status_code == 401


def test_reindex_stays_subject_to_existing_queue_limit(reindex_api):
    client, _, settings, requests = reindex_api
    settings.web_task_queue_limit = 0
    assert client.post("/api/v1/knowledge/reindex").status_code == 429
    assert requests == []


def test_desktop_reindex_retains_full_library_behavior(reindex_api):
    client, factory, settings, _ = reindex_api
    seed_papers(factory, 1, 4)
    seed_papers(factory, 2, 3)
    settings.web_mode = False
    response = client.post("/api/v1/knowledge/reindex")
    assert response.status_code == 200, response.text
    assert response.json()["indexed_papers"] == 7
    # Desktop's explicit rebuild still refreshes the complete current index.
    assert client.post("/api/v1/knowledge/reindex").json()["indexed_papers"] == 7
