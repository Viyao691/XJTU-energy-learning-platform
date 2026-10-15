from __future__ import annotations

import sqlite3
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def _set_sqlite_foreign_keys(
    dbapi_connection: object,
    _connection_record: object,
) -> None:
    if not isinstance(dbapi_connection, sqlite3.Connection):
        return
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=ON")
        if get_settings().web_mode:
            version = sqlite3.sqlite_version_info
            patched = version >= (3, 51, 3) or (3, 50, 7) <= version < (3, 51, 0) or (3, 44, 6) <= version < (3, 45, 0)
            if not patched:
                raise RuntimeError("Web WAL requires SQLite with the official WAL-reset fix")
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA busy_timeout=5000")
    finally:
        cursor.close()


def enable_sqlite_foreign_keys(engine: Engine) -> Engine:
    """Enable SQLite FK checks without changing other database backends."""
    if engine.dialect.name == "sqlite":
        event.listen(engine, "connect", _set_sqlite_foreign_keys)
    return engine


def ensure_database_directory() -> None:
    url = make_url(get_settings().database_url)
    if url.drivername.startswith("sqlite") and url.database and url.database != ":memory:":
        Path(url.database).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


def make_engine():
    ensure_database_directory()
    url = get_settings().database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, connect_args=connect_args)
    return enable_sqlite_foreign_keys(engine)


def make_session_factory():
    from app.ownership import OwnedSession
    return sessionmaker(bind=make_engine(), class_=OwnedSession, autoflush=False, autocommit=False)
