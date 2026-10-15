from __future__ import with_statement

from alembic import context
from sqlalchemy import engine_from_config, inspect, pool

from app.config import get_settings
from app.database import Base, enable_sqlite_foreign_keys
import app.models  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = enable_sqlite_foreign_keys(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
    )
    with connectable.connect() as connection:
        inspector = inspect(connection)
        ownership_upgrade = (
            connection.dialect.name == "sqlite"
            and inspector.has_table("papers")
            and "user_id" not in {column["name"] for column in inspector.get_columns("papers")}
        )
        connection.commit()
        if ownership_upgrade:
            # SQLite batch recreation must not cascade-delete existing children.
            # Toggle outside the transaction, then check every FK before return.
            connection.commit()
            connection.exec_driver_sql("PRAGMA foreign_keys=OFF")
            connection.commit()
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
        if ownership_upgrade:
            connection.commit()
            if connection.exec_driver_sql("PRAGMA foreign_key_check").first() is not None:
                raise RuntimeError("Ownership migration produced invalid foreign keys")
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")
            connection.commit()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
