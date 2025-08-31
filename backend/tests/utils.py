from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple
import uuid

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

    account_id = "a1"
    org_id = "o1"
    membership_id = "m1"
    email = "mgr@example.com"
    org_name = "Org"

    def try_insert(aid: str, oid: str, mid: str, mail: str, oname: str) -> bool:
        try:
            with eng.begin() as c:
                c.execute(text("PRAGMA foreign_keys = ON"))
                c.execute(
                    text(
                        "INSERT INTO orgs (id, name, created_at, updated_at) "
                        "VALUES (:id, :name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
                    ),
                    {"id": oid, "name": oname},
                )
                c.execute(
                    text(
                        "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) "
                        "VALUES (:id, :oid, :email, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
                    ),
                    {"id": aid, "oid": oid, "email": mail},
                )
                c.execute(
                    text(
                        "INSERT OR IGNORE INTO org_memberships (id, org_id, account_id, role, created_at, updated_at) "
                        "VALUES (:mid, :oid, :aid, 'manager', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
                    ),
                    {"mid": mid, "oid": oid, "aid": aid},
                )
            return True
        except Exception:
            return False

    if not try_insert(account_id, org_id, membership_id, email, org_name):
        suf = uuid.uuid4().hex[:8]
        account_id = f"a_{suf}"
        org_id = f"o_{suf}"
        membership_id = f"m_{suf}"
        email = f"mgr_{suf}@example.com"
        org_name = f"Org_{suf}"
        if not try_insert(account_id, org_id, membership_id, email, org_name):
            suf = uuid.uuid4().hex[:8]
            account_id = f"a_{suf}"
            org_id = f"o_{suf}"
            membership_id = f"m_{suf}"
            email = f"mgr_{suf}@example.com"
            org_name = f"Org_{suf}"
            if not try_insert(account_id, org_id, membership_id, email, org_name):
                raise RuntimeError(
                    "Impossible de creer org/account de test (UNIQUE conflict)"
                )

    return account_id, org_id
