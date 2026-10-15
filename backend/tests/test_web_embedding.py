from __future__ import annotations

import json
import math

import httpx
import pytest

from app.knowledge import EmbeddingProviderError, make_embedding_provider


def remote_provider(monkeypatch, payload, *, status=200):
    import app.knowledge as knowledge

    captured = []

    def handle(request):
        captured.append(request)
        return httpx.Response(status, content=json.dumps(payload), headers={"content-type": "application/json"})

    monkeypatch.setattr(knowledge, "_remote_embedding_client", lambda: httpx.Client(transport=httpx.MockTransport(handle)), raising=False)
    provider = make_embedding_provider(
        "openai_compatible", "https://embed.test/v1/", "embedding-v1", 30,
        api_key="embedding-test-secret", web_mode=False,
    )
    return provider, captured


def test_remote_embedding_orders_and_normalizes_vectors(monkeypatch):
    provider, captured = remote_provider(monkeypatch, {
        "data": [{"index": 1, "embedding": [0, 2]}, {"index": 0, "embedding": [3, 4]}],
    })

    assert provider.embed(["first", "second"]) == [[0.6, 0.8], [0, 1]]
    assert str(captured[0].url) == "https://embed.test/v1/embeddings"
    assert captured[0].headers["authorization"] == "Bearer embedding-test-secret"
    assert json.loads(captured[0].content) == {
        "model": "embedding-v1", "input": ["first", "second"], "encoding_format": "float",
    }
    assert provider.model_name == "openai_compatible:embedding-v1"
    assert "embedding-test-secret" not in repr(provider)


@pytest.mark.parametrize("data", [
    [],
    [{"index": 0, "embedding": [1, 0]}],
    [{"index": 0, "embedding": [1, 0]}, {"index": 0, "embedding": [0, 1]}],
    [{"index": 0, "embedding": [1, 0]}, {"index": 1, "embedding": [1, 0, 1]}],
    [{"index": 0, "embedding": [1, 0]}, {"index": 1, "embedding": [math.inf, 1]}],
    [{"index": 0, "embedding": [1, 0]}, {"index": 1, "embedding": [0, 0]}],
    [{"index": 0, "embedding": [1, 0]}, {"index": 1, "embedding": ["1", 0]}],
])
def test_remote_embedding_rejects_invalid_vectors(monkeypatch, data):
    provider, _ = remote_provider(monkeypatch, {"data": data})
    with pytest.raises(EmbeddingProviderError, match="格式无效"):
        provider.embed(["one", "two"])


def test_remote_embedding_rejects_dimension_change_across_batches(monkeypatch):
    provider, _ = remote_provider(monkeypatch, {"data": [{"index": 0, "embedding": [1, 0]}]})
    provider.embed(["one"])
    provider.client = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(
        200, json={"data": [{"index": 0, "embedding": [1, 0, 0]}]},
    )))
    with pytest.raises(EmbeddingProviderError, match="格式无效"):
        provider.embed(["two"])


def test_remote_failure_is_safe_and_does_not_fallback(monkeypatch):
    provider, _ = remote_provider(monkeypatch, {"error": "embedding-test-secret"}, status=401)
    with pytest.raises(EmbeddingProviderError) as caught:
        provider.embed(["one"])
    assert "embedding-test-secret" not in str(caught.value)
    assert provider.test_connection()[0] is False


@pytest.mark.parametrize("name,key", [("mock", ""), ("ollama", ""), ("openai_compatible", "")])
def test_web_unconfigured_embeddings_are_unavailable(name, key):
    provider = make_embedding_provider(name, "https://embed.test/v1", "embedding-v1", 30, api_key=key, web_mode=True)
    assert provider.test_connection()[0] is False
    with pytest.raises(EmbeddingProviderError, match="尚未配置"):
        provider.embed(["question"])


def test_desktop_mock_factory_keeps_existing_behavior():
    provider = make_embedding_provider("mock", "http://ollama.test", "unused", 30, web_mode=False)
    assert provider.name == "mock"
    assert len(provider.embed(["hello"])[0]) == 384
