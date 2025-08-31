from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

TEST_DB_PATH = Path("backend/test_avail.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"


def _cleanup() -> None:
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink(missing_ok=True)
        except PermissionError:
            pass


def _upgrade(url: str) -> None:
    _cleanup()
    os.environ["DB_URL"] = url
    os.environ["DATABASE_URL"] = url
    cfg = Config("backend/alembic.ini")
    command.upgrade(cfg, "head")


def _client() -> TestClient:
    from app.main import create_app
    from app.auth import get_current_account

    app = create_app()
    app.dependency_overrides[get_current_account] = lambda: {
        "id": "a1",
        "org_id": "o1",
        "email": "mgr@example.com",
    }
    return TestClient(app)


def _mk_account_and_members(db_url: str) -> Tuple[str, str]:
    eng = create_engine(db_url, future=True)
    with eng.begin() as c:
        c.execute(
            text(
                "INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('o1','Org',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        c.execute(
            text(
                "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) VALUES ('a1','o1','mgr@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        c.execute(
            text(
                "INSERT INTO org_memberships (id, org_id, account_id, role, created_at, updated_at) VALUES ('m1','o1','a1','manager',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
    return "a1", "o1"
