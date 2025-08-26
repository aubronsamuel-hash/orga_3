from __future__ import annotations

import gc
import os
import time
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

TEST_DB_PATH = Path("backend/test_unique.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"


def _unlink_with_retry(p: Path, attempts: int = 10, delay_s: float = 0.1) -> None:
    for _ in range(attempts):
        try:
            p.unlink(missing_ok=True)
            return
        except PermissionError:
            gc.collect()
            time.sleep(delay_s)
    p.unlink(missing_ok=True)


def setup_module(module) -> None:  # noqa: ANN001
    if TEST_DB_PATH.exists():
        _unlink_with_retry(TEST_DB_PATH)


def teardown_module(module) -> None:  # noqa: ANN001
    if TEST_DB_PATH.exists():
        _unlink_with_retry(TEST_DB_PATH)


def _alembic_upgrade(url: str) -> None:
    os.environ["DB_URL"] = url
    cfg = Config("backend/alembic.ini")
    cfg.set_main_option("script_location", "backend/alembic")
    command.upgrade(cfg, "head")


def test_unique_active_assignment_ok_and_ko() -> None:
    _alembic_upgrade(TEST_DB_URL)
    eng = create_engine(TEST_DB_URL, future=True)
    try:
        with eng.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('o1','Org',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                )
            )
            conn.execute(
                text(
                    "INSERT INTO users (id, org_id, first_name, last_name, employment_type, created_at, updated_at) VALUES ('u1','o1','Sam','A','Intermittent',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                )
            )
            conn.execute(
                text(
                    "INSERT INTO missions (id, org_id, title, starts_at, ends_at, created_at, updated_at) VALUES ('m1','o1','Balance','2024-01-01T10:00:00','2024-01-01T12:00:00',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                )
            )

            conn.execute(
                text(
                    "INSERT INTO assignments (id, mission_id, user_id, status, created_at, updated_at) VALUES ('a1','m1','u1','INVITED',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                )
            )
            conn.execute(
                text(
                    "INSERT INTO assignments (id, mission_id, user_id, status, created_at, updated_at) VALUES ('a2','m1','u1','CANCELLED',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                )
            )

            try:
                conn.execute(
                    text(
                        "INSERT INTO assignments (id, mission_id, user_id, status, created_at, updated_at) VALUES ('a3','m1','u1','ACCEPTED',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                    )
                )
                assert False, "Devrait violer l index unique partiel pour ACTIVE"
            except Exception as e:
                assert isinstance(e, IntegrityError) or "UNIQUE constraint failed" in str(e)
    finally:
        eng.dispose()
