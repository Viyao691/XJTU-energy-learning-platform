"""Small web-only limits; desktop storage and parsing stay unchanged."""
import asyncio
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from threading import Lock

from fastapi import HTTPException

from app.config import get_settings
from app.ownership import current_user_id


_NATIVE_PARSE_LOCK = Lock()
WEB_MAX_EXTRACTED_CHARS = 2_000_000


def assert_owned_storage_capacity(incoming: int, ignore_path: Path | None = None) -> None:
    settings = get_settings()
    if not settings.web_mode:
        return
    if current_user_id.get() is None:
        raise HTTPException(401, "请先登录")
    root = settings.paper_storage_dir.resolve()
    ignored = ignore_path.resolve() if ignore_path is not None else None
    used = sum(
        path.stat().st_size for path in root.rglob("*")
        if path.is_file() and path.suffix != ".tmp" and path.resolve() != ignored
        and path.resolve().is_relative_to(root)
    )
    if used + incoming > settings.web_user_storage_mb * 1024 * 1024:
        raise HTTPException(413, "个人存储空间已满，请先删除不需要的文件")


@contextmanager
def native_parse_slot():
    if get_settings().web_mode:
        with _NATIVE_PARSE_LOCK:
            yield
    else:
        yield


@asynccontextmanager
async def async_native_parse_slot():
    if not get_settings().web_mode:
        yield
        return
    while not _NATIVE_PARSE_LOCK.acquire(blocking=False):
        await asyncio.sleep(0.05)
    try:
        yield
    finally:
        _NATIVE_PARSE_LOCK.release()
