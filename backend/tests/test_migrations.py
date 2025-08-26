from __future__ import annotations
import os
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

def setup_module(module) -> None:  # noqa: ANN001
    # Nettoyage ancien fichier
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink(missing_ok=True)

def teardown_module(module) -> None:  # noqa: ANN001
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink(missing_ok=True)

def test_upgrade_and_downgrade_base() -> None:
    cfg = _alembic_config_with_url(TEST_DB_URL)
    # Upgrade head
    command.upgrade(cfg, "head")
    # Verifier existence de la table
    engine = create_engine(TEST_DB_URL, future=True)
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_meta'")
        ).fetchone()
        assert res is not None, "schema_meta devrait exister apres upgrade"

    # Downgrade base
    command.downgrade(cfg, "base")
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_meta'")
        ).fetchone()
        assert res is None, "schema_meta ne devrait plus exister apres downgrade"
