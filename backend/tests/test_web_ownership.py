from pathlib import Path

import pytest
from sqlalchemy import create_engine, delete, func, select, update


def test_scoped_session_filters_reads_writes_and_duplicate_papers(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    from app.config import reset_settings_cache
    reset_settings_cache()
    from app.database import Base
    from app.models import Paper, Note
    from app.ownership import OwnedSession

    engine = create_engine(f"sqlite:///{tmp_path / 'ownership.db'}")
    Base.metadata.create_all(engine)
    with OwnedSession(bind=engine, user_id=1) as db:
        paper = Paper(title="first", file_size=10, file_hash="same")
        db.add(paper)
        db.commit()
        first_id = paper.id
        db.add(Note(paper_id=first_id, content="private"))
        db.commit()
    with OwnedSession(bind=engine, user_id=2) as db:
        assert db.get(Paper, first_id) is None
        assert db.scalar(select(func.count(Paper.id))) == 0
        assert db.scalars(select(Note)).all() == []
        assert db.execute(update(Paper).where(Paper.id == first_id).values(title="stolen")).rowcount == 0
        assert db.execute(delete(Note).where(Note.paper_id == first_id)).rowcount == 0
        db.add(Paper(title="second", file_size=10, file_hash="same"))
        db.commit()
        assert len(db.scalars(select(Paper)).all()) == 1
    with OwnedSession(bind=engine, user_id=1) as db:
        assert db.get(Paper, first_id).title == "first"
        assert db.scalar(select(Note)).content == "private"
    with OwnedSession(bind=engine) as db:
        assert db.scalars(select(Paper)).all() == []
        db.add(Paper(title="anonymous", file_size=0))
        with pytest.raises(PermissionError):
            db.commit()
    engine.dispose()
    reset_settings_cache()


def test_cross_user_parent_reference_and_owner_reassignment_rejected(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("ENERGY_WEB_MODE", "true")
    from app.config import reset_settings_cache
    reset_settings_cache()
    from app.database import Base
    from app.models import Paper, Note
    from app.ownership import OwnedSession

    engine = create_engine(f"sqlite:///{tmp_path / 'relations.db'}")
    Base.metadata.create_all(engine)
    with OwnedSession(bind=engine, user_id=1) as db:
        paper = Paper(title="first", file_size=0)
        db.add(paper)
        db.commit()
        first_id = paper.id
        paper.user_id = 2
        with pytest.raises(PermissionError):
            db.commit()
    with OwnedSession(bind=engine, user_id=2) as db:
        db.add(Note(paper_id=first_id, content="foreign"))
        with pytest.raises(PermissionError):
            db.commit()
    engine.dispose()
    reset_settings_cache()
