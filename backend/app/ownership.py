"""Web-only ownership boundaries; desktop rows retain owner zero."""
from contextvars import ContextVar

from sqlalchemy import Integer, event, inspect
from sqlalchemy.orm import Mapped, Session, mapped_column, with_loader_criteria
from sqlalchemy.sql.elements import TextClause

from app.config import get_settings


current_user_id: ContextVar[int | None] = ContextVar("energy_user_id", default=None)


class OwnedRow:
    user_id: Mapped[int] = mapped_column(Integer, default=0, server_default="0", index=True)


class OwnedSession(Session):
    def __init__(self, *args, user_id: int | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.info["web_scope"] = getattr(get_settings(), "web_mode", False)
        self.info["user_id"] = user_id if user_id is not None else current_user_id.get()


@event.listens_for(OwnedSession, "do_orm_execute")
def scope_query(state):
    if not state.session.info["web_scope"]:
        return
    owner = state.session.info["user_id"] or -1
    if isinstance(state.statement, TextClause):
        raise PermissionError("Web 私有查询必须使用受管 ORM 会话")
    if state.is_select:
        state.statement = state.statement.options(
            with_loader_criteria(OwnedRow, lambda row: row.user_id == owner, include_aliases=True)
        )
    elif state.is_update or state.is_delete:
        mapper = state.bind_mapper
        if mapper is not None and issubclass(mapper.class_, OwnedRow):
            if state.is_update and any(getattr(key, "name", key) == "user_id" for key in (state.statement._values or {})):
                raise PermissionError("不能修改记录所属用户")
            state.statement = state.statement.where(mapper.class_.user_id == owner)
    elif state.is_insert and state.bind_mapper is not None and issubclass(state.bind_mapper.class_, OwnedRow):
        raise PermissionError("私有记录必须通过受管对象创建")


@event.listens_for(OwnedSession, "before_flush")
def scope_changes(db, _context, _instances):
    if not db.info["web_scope"]:
        return
    owner = db.info["user_id"]
    for item in set(db.new) | set(db.dirty) | set(db.deleted):
        if not isinstance(item, OwnedRow):
            continue
        if not owner:
            raise PermissionError("私有记录需要已登录用户")
        if item in db.new and item.user_id is None:
            item.user_id = owner
        if item.user_id != owner:
            raise PermissionError("不能访问其他用户的记录")
        mapper = inspect(type(item))
        for column in mapper.columns:
            parent_id = getattr(item, column.key)
            if parent_id is None:
                continue
            parent_tables = [fk.column.table for fk in column.foreign_keys]
            # A few original desktop relations predate explicit foreign keys.
            if not parent_tables and column.key == "paper_id":
                parent_tables = [mapper.local_table.metadata.tables["papers"]]
            for table in parent_tables:
                if "user_id" not in table.c:
                    continue
                with db.no_autoflush:
                    found = db.connection().execute(
                        table.select().with_only_columns(table.c.user_id).where(table.c.id == parent_id)
                    ).scalar_one_or_none()
                if found is not None and found != owner:
                    raise PermissionError("关联记录不属于当前用户")
