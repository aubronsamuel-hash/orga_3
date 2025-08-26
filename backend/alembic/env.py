from __future__ import annotations
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Config Alembic

config = context.config

# Logging config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# URL prioritaire: env DATABASE_URL sinon valeur d env alembic DB_URL sinon fallback SQLite

db_url = os.getenv("DATABASE_URL") or os.getenv("DB_URL") or "sqlite:///./backend/dev.db"
config.set_main_option("sqlalchemy.url", db_url)

# Pas d autogenerate au jalon 2 (schema min gere via operations scripts)

target_metadata = None

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    try:
        with connectable.connect() as connection:
            context.configure(connection=connection)
            with context.begin_transaction():
                context.run_migrations()
    finally:
        # Important sous Windows/SQLite: libere les poignees de fichiers
        try:
            connectable.dispose()
        except Exception:
            # Pas bloquant: on evite d echouer le pipeline si la disposal echoue
            pass

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
