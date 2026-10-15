from pathlib import Path

import pytest
from fastapi import HTTPException


@pytest.fixture()
def web_storage(tmp_path, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    monkeypatch.setenv("PAPER_STORAGE_PATH", str(tmp_path / "papers"))
    monkeypatch.setenv("WEB_USER_STORAGE_MB", "1")
    from app.config import get_settings, reset_settings_cache
    from app.ownership import current_user_id
    reset_settings_cache()
    token = current_user_id.set(1)
    root = get_settings().paper_storage_dir
    root.mkdir(parents=True)
    yield root
    current_user_id.reset(token)
    reset_settings_cache()


def test_capacity_includes_tables_exports_but_not_other_users_or_temporary(web_storage):
    from app.web_limits import assert_owned_storage_capacity
    root = web_storage
    (root / "scientific-imports").mkdir()
    (root / "research-exports").mkdir()
    (root / "scientific-imports" / "data.csv").write_bytes(b"x" * 400_000)
    (root / "research-exports" / "report.md").write_bytes(b"x" * 400_000)
    (root / "upload.tmp").write_bytes(b"x" * 2_000_000)
    other = root.parents[1] / "2" / "papers"
    other.mkdir(parents=True)
    (other / "private.pdf").write_bytes(b"x" * 2_000_000)
    assert_owned_storage_capacity(200_000)
    with pytest.raises(HTTPException) as failure:
        assert_owned_storage_capacity(300_000)
    assert failure.value.status_code == 413


def test_capacity_rejects_missing_tenant_in_web_mode(web_storage):
    from app.ownership import current_user_id
    from app.web_limits import assert_owned_storage_capacity
    token = current_user_id.set(None)
    try:
        with pytest.raises(HTTPException) as failure:
            assert_owned_storage_capacity(1)
        assert failure.value.status_code == 401
    finally:
        current_user_id.reset(token)


def test_desktop_storage_capacity_is_unchanged(web_storage, monkeypatch):
    from app.config import reset_settings_cache
    from app.web_limits import assert_owned_storage_capacity
    monkeypatch.setenv("ENERGY_WEB_MODE", "false")
    reset_settings_cache()
    assert_owned_storage_capacity(10_000_000)


def test_capacity_ignores_explicit_download_stage(web_storage):
    from app.web_limits import assert_owned_storage_capacity
    stage = web_storage / "incoming.stage"
    stage.write_bytes(b"x" * 800_000)
    assert_owned_storage_capacity(800_000, ignore_path=stage)
    with pytest.raises(HTTPException):
        assert_owned_storage_capacity(800_000)


def test_native_parse_slots_serialize_threads(web_storage):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    from app.web_limits import native_parse_slot
    first_entered, release_first, second_entered = Event(), Event(), Event()
    def first():
        with native_parse_slot():
            first_entered.set()
            assert release_first.wait(2)
    def second():
        with native_parse_slot():
            second_entered.set()
    with ThreadPoolExecutor(max_workers=2) as pool:
        first_job = pool.submit(first)
        assert first_entered.wait(2)
        second_job = pool.submit(second)
        assert not second_entered.wait(0.05)
        release_first.set()
        first_job.result()
        second_job.result()
    assert second_entered.is_set()


def test_native_pdf_rejects_accumulated_text_without_truncation(web_storage, monkeypatch):
    from app.routers import _shared
    class Page:
        def get_text(self, mode):
            return "x" * 1_000_001
    class Document:
        closed = False
        def __len__(self):
            return 2
        def __iter__(self):
            return iter([Page(), Page()])
        def close(self):
            self.closed = True
    document = Document()
    monkeypatch.setattr(_shared.fitz, "open", lambda path: document)
    monkeypatch.setattr("app.paper_metadata.pdf_bibliography_metadata", lambda document: {})
    with pytest.raises(HTTPException) as failure:
        _shared._extract_pdf(Path("synthetic.pdf"))
    assert failure.value.status_code == 413
    assert document.closed


def test_download_capacity_rejects_before_publication_and_cleans_stage(web_storage, monkeypatch):
    import asyncio
    import httpx
    from app.services import paper_download
    root = web_storage
    (root / "data.csv").write_bytes(b"x" * (1024 * 1024 - 10))
    pdf = b"%PDF-" + b"x" * 100
    async def parsed(path):
        return "text", 1, 1.0, None, "已读取全文"
    monkeypatch.setattr(paper_download, "_extract_pdf_in_process", parsed)
    async def scenario():
        transport = httpx.MockTransport(lambda request: httpx.Response(
            200, headers={"Content-Type": "application/pdf"}, stream=httpx.ByteStream(pdf)))
        async with httpx.AsyncClient(transport=transport) as client:
            await paper_download._download_pdf_with_client(
                "https://papers.example/paper.pdf", root, client,
                timeout_seconds=5, max_size_mb=1, dns_resolver=lambda *_: ["93.184.216.34"])
    with pytest.raises(HTTPException) as failure:
        asyncio.run(scenario())
    assert failure.value.status_code == 413
    assert not list(root.glob("*.pdf"))
    assert not list(root.glob("*.tmp"))
