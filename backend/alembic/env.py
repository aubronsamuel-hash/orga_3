from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool, create_engine
from sqlalchemy.pool import StaticPool
from alembic import context


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def run_migrations_offline() -> None:
    url = (
        os.getenv("ALEMBIC_URL")
        or os.getenv("DATABASE_URL")
        or config.get_main_option("sqlalchemy.url")
    )
    if url:
        config.set_main_option("sqlalchemy.url", url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = (
        os.getenv("ALEMBIC_URL")
        or os.getenv("DATABASE_URL")
        or config.get_main_option("sqlalchemy.url")
    )
    if url:
        config.set_main_option("sqlalchemy.url", url)

    if url and url.startswith("sqlite") and (
        ":memory:" in url or "mode=memory" in url
    ):
        connectable = create_engine(
            url,
            future=True,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
    else:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

