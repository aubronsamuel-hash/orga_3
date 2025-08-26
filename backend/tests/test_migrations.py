from __future__ import annotations
import gc
import os
import time
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text

TEST_DB_PATH = Path("backend/test_migrations.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

def _alembic_config_with_url(db_url: str) -> Config:
    cfg = Config("backend/alembic.ini")
    cfg.set_main_option("script_location", "backend/alembic")
    # Variable d env attendue par alembic.ini (DB_URL)
    os.environ["DB_URL"] = db_url
    return cfg

def _unlink_with_retry(p: Path, attempts: int = 10, delay_s: float = 0.1) -> None:
    for _ in range(attempts):
        try:
            p.unlink(missing_ok=True)
            return
        except PermissionError:
            gc.collect()
            time.sleep(delay_s)
    # Derniere tentative explicite (laissera l erreur si encore verrouille)
    p.unlink(missing_ok=True)

def setup_module(module) -> None:  # noqa: ANN001
    if TEST_DB_PATH.exists():
        _unlink_with_retry(TEST_DB_PATH)

def teardown_module(module) -> None:  # noqa: ANN001
    if TEST_DB_PATH.exists():
        _unlink_with_retry(TEST_DB_PATH)

def test_upgrade_and_downgrade_base() -> None:
    cfg = _alembic_config_with_url(TEST_DB_URL)

    # Upgrade head
    command.upgrade(cfg, "head")

    # Verifier existence de la table avec un engine dedie
    engine = create_engine(TEST_DB_URL, future=True)
    try:
        with engine.connect() as conn:
            res = conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_meta'")
            ).fetchone()
            assert res is not None, "schema_meta devrait exister apres upgrade"
    finally:
        # Libere le handle de fichier sous Windows/SQLite
        engine.dispose()

    # Downgrade base
    command.downgrade(cfg, "base")

    # Nouveau engine pour verifier suppression
    engine2 = create_engine(TEST_DB_URL, future=True)
    try:
        with engine2.connect() as conn:
            res = conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_meta'")
            ).fetchone()
            assert res is None, "schema_meta ne devrait plus exister apres downgrade"
    finally:
        engine2.dispose()

