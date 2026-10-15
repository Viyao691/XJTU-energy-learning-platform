from datetime import datetime
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float, Integer


def test_ownership_migration_preserves_legacy_paper_and_note(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'legacy.db'}")
    monkeypatch.setenv("ENERGY_WEB_MODE", "false")
    from app.config import reset_settings_cache
    reset_settings_cache()
    config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    command.upgrade(config, "0029")
    engine = create_engine(f"sqlite:///{tmp_path / 'legacy.db'}")
    metadata = MetaData()
    paper = Table("papers", metadata, autoload_with=engine)
    note = Table("notes", metadata, autoload_with=engine)
    source = Table("paper_source_records", metadata, autoload_with=engine)

    def required(table):
        result = {}
        for column in table.c:
            if column.primary_key or column.nullable or column.server_default:
                continue
            result[column.name] = (
                datetime.utcnow() if isinstance(column.type, DateTime) else
                False if isinstance(column.type, Boolean) else
                0 if isinstance(column.type, (Integer, Float)) else ""
            )
        return result

    with engine.begin() as db:
        db.execute(paper.insert().values(**(required(paper) | {"id": 1, "title": "legacy paper"})))
        db.execute(note.insert().values(**(required(note) | {"paper_id": 1, "content": "keep my note"})))
        db.execute(source.insert().values(**(required(source) | {"paper_id": 1, "source": "crossref", "external_id": "legacy"})))
    command.upgrade(config, "head")
    with engine.connect() as db:
        assert db.exec_driver_sql("SELECT title, user_id FROM papers").one() == ("legacy paper", 0)
        assert db.exec_driver_sql("SELECT content, user_id FROM notes").one() == ("keep my note", 0)
        assert db.exec_driver_sql("SELECT external_id, user_id FROM paper_source_records").one() == ("legacy", 0)
        assert db.exec_driver_sql("PRAGMA foreign_key_check").all() == []
    engine.dispose()
    reset_settings_cache()
