from pathlib import Path

import fitz
import pytest
from fastapi import HTTPException


def test_web_rejects_excess_pdf_pages_before_extraction(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    monkeypatch.setenv("WEB_MAX_PDF_PAGES", "1")
    from app.config import reset_settings_cache
    reset_settings_cache()
    from app.routers._shared import _extract_pdf
    document = fitz.open()
    document.new_page()
    document.new_page()
    path = tmp_path / "two.pdf"
    document.save(path)
    document.close()
    with pytest.raises(HTTPException) as failure:
        _extract_pdf(path)
    assert failure.value.status_code == 413
    reset_settings_cache()
