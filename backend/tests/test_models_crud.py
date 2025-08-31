from __future__ import annotations

import gc
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

TEST_DB_PATH = Path("backend/test_models.db").resolve()
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


def test_crud_minimal_flow() -> None:
    _alembic_upgrade(TEST_DB_URL)
    engine = create_engine(TEST_DB_URL, future=True)
    from app.enums import AssignmentStatus, ProjectStatus  # import after upgrade
    _ = (AssignmentStatus, ProjectStatus)

    with Session(engine, future=True) as s:
        # Org
        s.execute(
            text(
                "INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('org1','Org A',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        # Account
        s.execute(
            text(
                "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) VALUES ('acc1','org1','a@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        # User
        s.execute(
            text(
                "INSERT INTO users (id, org_id, account_id, first_name, last_name, employment_type, created_at, updated_at) VALUES ('u1','org1','acc1','Sam','A','Intermittent',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        # Project
        s.execute(
            text(
                "INSERT INTO projects (id, org_id, name, status, created_at, updated_at) VALUES ('p1','org1','Projet X','DRAFT',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        # Mission
        now = datetime.utcnow()
        later = now + timedelta(hours=2)
        s.execute(
            text(
                "INSERT INTO missions (id, org_id, project_id, title, starts_at, ends_at, created_at, updated_at) VALUES ('m1','org1','p1','Balance','%s','%s',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                % (now.isoformat(), later.isoformat())
            )
        )
        # Role
        s.execute(
            text(
                "INSERT INTO mission_roles (id, mission_id, role_name, quota, created_at, updated_at) VALUES ('mr1','m1','Regie','1',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        # Assignment INVITED
        s.execute(
            text(
                "INSERT INTO assignments (id, mission_id, user_id, status, created_at, updated_at) VALUES ('a1','m1','u1','INVITED',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        # Availability
        s.execute(
            text(
                "INSERT INTO availability (id, org_id, user_id, starts_at, ends_at, created_at, updated_at) VALUES ('av1','org1','u1','%s','%s',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
                % (now.isoformat(), later.isoformat())
            )
        )

        res = s.execute(text("SELECT COUNT(*) FROM assignments")).scalar_one()
        assert res == 1
        res = s.execute(text("SELECT status FROM assignments WHERE id='a1'")).scalar_one()
        assert res == "INVITED"

    engine.dispose()
