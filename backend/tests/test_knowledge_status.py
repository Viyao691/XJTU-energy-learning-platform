from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture()
def status_api(tmp_path, monkeypatch):
    from app.database import Base
    from app import knowledge, web_model, ownership
    from app.routers import knowledge as routes
    from app.ownership import OwnedSession

    settings = SimpleNamespace(web_mode=True, embedding_provider="openai_compatible",
                               embedding_base_url="https://embedding.test/v1", embedding_model="bge-m3",
                               embedding_timeout_seconds=30, embedding_api_key=SecretStr("test-key"),
                               web_embedding_call_reserve_cny=0.001)
    monkeypatch.setattr(routes, "get_settings", lambda: settings)
    monkeypatch.setattr(ownership, "get_settings", lambda: settings)
    monkeypatch.setattr(web_model, "wrap_web_embedding_provider", lambda provider: provider)
    original_factory = knowledge.make_embedding_provider

    def forbidden(*args, **kwargs):
        raise AssertionError("GET knowledge/status must not test or call an embedding service")

    def provider_factory(*args):
        provider = original_factory(*args, api_key=settings.embedding_api_key.get_secret_value(), web_mode=settings.web_mode)
        provider.test_connection = forbidden
        provider.embed = forbidden
        return provider

    monkeypatch.setattr(routes, "make_embedding_provider", provider_factory)
    engine = create_engine(f"sqlite:///{tmp_path / 'status.db'}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, class_=OwnedSession, expire_on_commit=False)
    api = FastAPI()

    def get_db():
        with factory(user_id=1) as db:
            yield db

    routes.register_knowledge_routes(api, get_db)
    with TestClient(api) as client:
        yield client, settings, factory
    engine.dispose()


@pytest.mark.parametrize("web_mode,provider,key,ready", [
    (True, "openai_compatible", "test-key", True),
    (True, "openai_compatible", "", False),
    (True, "ollama", "", False),
    (False, "ollama", "", True),
    (False, "mock", "", True),
])
def test_status_checks_configuration_without_network_or_embedding(status_api, web_mode, provider, key, ready):
    client, settings, _ = status_api
    settings.web_mode, settings.embedding_provider = web_mode, provider
    settings.embedding_api_key = SecretStr(key)
    response = client.get("/api/v1/knowledge/status")
    assert response.status_code == 200
    assert response.json()["ready"] is ready
    assert "test-key" not in response.text
    if ready:
        assert "未验证" in response.json()["message"] or "演示" in response.json()["message"]
    else:
        assert "管理员" in response.json()["message"]


def test_status_reports_missing_embedding_budget_without_paid_probe(status_api):
    client, settings, _ = status_api
    settings.web_embedding_call_reserve_cny = 0
    response = client.get("/api/v1/knowledge/status")
    assert response.status_code == 200
    assert response.json()["ready"] is False
    assert "费用预留" in response.json()["message"]


def test_status_preserves_private_index_counts(status_api):
    from app.models import Paper, PaperChunk
    client, _, factory = status_api
    for owner in (1, 2):
        with factory(user_id=owner) as db:
            paper = Paper(title=f"private {owner}", file_size=0)
            db.add(paper)
            db.flush()
            db.add(PaperChunk(paper_id=paper.id, page_number=1, chunk_index=0, section="",
                              content="evidence", content_hash=f"hash{owner}", source_scope="fulltext",
                              parse_confidence=1, embedding_json="[1]", embedding_model="openai_compatible:bge-m3"))
            db.commit()
    payload = client.get("/api/v1/knowledge/status").json()
    assert payload["ready"] is True
    assert payload["total_papers"] == 1
    assert payload["indexed_papers"] == 1
    assert payload["chunk_count"] == 1
    assert payload["stale_papers"] == 0
