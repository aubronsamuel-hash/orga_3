from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Tuple

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from backend.app.auth import create_access_token

TEST_DB_PATH = Path("backend/test_invitations_accept.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"


def _engine(db_url: str) -> Engine:
    return create_engine(db_url, future=True)


def _cleanup(db_url: str) -> None:
    """Nettoyage idempotent des tables entre tests."""
    eng = _engine(db_url)
    with eng.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys = ON"))
        _cleanup_order = [
            "invitations",
            "assignments",
            "missions",
            "projects",
            "users",
            "org_memberships",
            "orgs",
            "accounts",
        ]
        for table in _cleanup_order:
            try:
                conn.execute(text(f"DELETE FROM {table}"))
            except Exception:
                pass


def _upgrade(url: str) -> None:
    os.environ["DB_URL"] = url
    os.environ["DATABASE_URL"] = url
    cfg = Config("backend/alembic.ini")
    command.upgrade(cfg, "head")


def _client() -> TestClient:
    from backend.app.main import create_app

    app = create_app()
    return TestClient(app)


def _mk_account_and_members(db_url: str) -> Tuple[str, str]:
    eng = _engine(db_url)
    uniq = uuid.uuid4().hex[:8]
    account_id = f"a_{uniq}"
    org_id = f"o_{uniq}"
    membership_id = f"m_{uniq}"
    email = f"user_{uniq}@example.com"
    org_name = f"Org_{uniq}"
    with eng.begin() as c:
        c.execute(text("PRAGMA foreign_keys = ON"))
        c.execute(
            text(
                "INSERT INTO orgs (id, name, created_at, updated_at) "
                "VALUES (:id, :name, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
            ),
            {"id": org_id, "name": org_name},
        )
        c.execute(
            text(
                "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) "
                "VALUES (:id, :org_id, :email, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
            ),
            {"id": account_id, "org_id": org_id, "email": email},
        )
        c.execute(
            text(
                "INSERT INTO org_memberships (id, org_id, account_id, role, created_at, updated_at) "
                "VALUES (:mid, :oid, :aid, 'manager', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
            ),
            {"mid": membership_id, "oid": org_id, "aid": account_id},
        )
    return account_id, org_id


def test_accept_invitation_ok() -> None:
    os.environ["ENV"] = "dev"
    _cleanup(TEST_DB_URL)
    _upgrade(TEST_DB_URL)
    acc, org = _mk_account_and_members(TEST_DB_URL)
    token = create_access_token(acc, org)

    client = _client()

    r = client.post(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Alice"},
    )
    assert r.status_code == 200
    user_id = r.json()["id"]

    r = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "P1", "status": "ACTIVE"},
    )
    assert r.status_code == 200
    pid = r.json()["id"]

    items = [
        {"start_at": "2025-09-01T09:00:00Z", "end_at": "2025-09-01T18:00:00Z", "role": "tech"},
        {"start_at": "2025-09-02T09:00:00Z", "end_at": "2025-09-02T18:00:00Z", "role": "tech"},
    ]
    r = client.post(
        f"/api/v1/projects/{pid}/missions:bulk_create",
        headers={"Authorization": f"Bearer {token}"},
        json=items,
    )
    assert r.status_code == 200

    r = client.get("/api/v1/missions", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    m1 = r.json()[0]["id"]

    r = client.post(
        "/api/v1/assignments",
        headers={"Authorization": f"Bearer {token}"},
        json={"mission_id": m1, "user_id": user_id},
    )
    assert r.status_code == 200
    aid = r.json()["id"]

    r = client.post(
        "/api/v1/invitations",
        headers={"Authorization": f"Bearer {token}"},
        json={"assignment_id": aid, "email": "alice@example.com"},
    )
    assert r.status_code == 200
    inv_id = r.json()["id"]
    inv_tok = r.json()["token"]

    r = client.post(f"/api/v1/invitations/{inv_id}/accept", params={"token": inv_tok})
    assert r.status_code == 200
    body = r.json()
    assert body["accepted"] is True
    assert body["invitation_id"] == inv_id
    assert body["assignment_id"] == aid


def test_accept_invitation_ko_wrong_token() -> None:
    os.environ["ENV"] = "dev"
    _cleanup(TEST_DB_URL)
    _upgrade(TEST_DB_URL)
    acc, org = _mk_account_and_members(TEST_DB_URL)
    token = create_access_token(acc, org)

    client = _client()

    r = client.post(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Bob"},
    )
    assert r.status_code == 200
    user_id = r.json()["id"]

    r = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "P1", "status": "ACTIVE"},
    )
    assert r.status_code == 200
    pid = r.json()["id"]

    items = [
        {"start_at": "2025-09-01T09:00:00Z", "end_at": "2025-09-01T18:00:00Z", "role": "tech"}
    ]
    r = client.post(
        f"/api/v1/projects/{pid}/missions:bulk_create",
        headers={"Authorization": f"Bearer {token}"},
        json=items,
    )
    assert r.status_code == 200

    r = client.get("/api/v1/missions", headers={"Authorization": f"Bearer {token}"})
    m1 = r.json()[0]["id"]

    r = client.post(
        "/api/v1/assignments",
        headers={"Authorization": f"Bearer {token}"},
        json={"mission_id": m1, "user_id": user_id},
    )
    aid = r.json()["id"]

    r = client.post(
        "/api/v1/invitations",
        headers={"Authorization": f"Bearer {token}"},
        json={"assignment_id": aid, "email": "bob@example.com"},
    )
    inv_id = r.json()["id"]

    r = client.post(
        f"/api/v1/invitations/{inv_id}/accept",
        params={"token": "WRONGTOKEN"},
    )
    assert r.status_code in (400, 404)
