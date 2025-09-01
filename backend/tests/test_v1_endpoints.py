from __future__ import annotations
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.auth import create_access_token

TEST_DB_PATH = Path("backend/test_v1.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

def _cleanup() -> None:
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink(missing_ok=True)
        except PermissionError:
            pass

def setup_module(module) -> None:  # noqa: ANN001
    _cleanup()

def teardown_module(module) -> None:  # noqa: ANN001
    _cleanup()

def _upgrade(url: str) -> None:
    os.environ["DB_URL"] = url
    os.environ["DATABASE_URL"] = url
    cfg = Config("backend/alembic.ini")
    command.upgrade(cfg, "head")

def _client():
    from app.main import create_app
    app = create_app()
    return TestClient(app)

def _mk_account_and_members(db_url: str):
    eng = create_engine(db_url, future=True)
    with eng.begin() as c:
        c.execute(text("INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('o1','Org',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        c.execute(text("INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) VALUES ('a1','o1','mgr@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        c.execute(text("INSERT INTO org_memberships (id, org_id, account_id, role, created_at, updated_at) VALUES ('m1','o1','a1','manager',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
    return "a1","o1"

def test_flow_project_bulk_missions_invite_accept_and_conflicts() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)
    acc, org = _mk_account_and_members(TEST_DB_URL)
    token = create_access_token(acc, org)

    client = _client()

    # Create user
    r = client.post("/api/v1/users", headers={"Authorization": f"Bearer {token}"}, json={"name":"Alice"})
    assert r.status_code == 200
    user_id = r.json()["id"]

    # Create project
    r = client.post("/api/v1/projects", headers={"Authorization": f"Bearer {token}"}, json={"name":"P1","status":"ACTIVE"})
    assert r.status_code == 200
    pid = r.json()["id"]

    # Bulk create 2 missions
    items = [
        {"start_at":"2025-09-01T09:00:00Z","end_at":"2025-09-01T18:00:00Z","role":"tech"},
        {"start_at":"2025-09-02T09:00:00Z","end_at":"2025-09-02T18:00:00Z","role":"tech"},
    ]
    r = client.post(f"/api/v1/projects/{pid}/missions:bulk_create", headers={"Authorization": f"Bearer {token}"}, json=items)
    assert r.status_code == 200

    # List missions & pick first
    r = client.get("/api/v1/missions", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    missions = r.json()
    assert len(missions) >= 2
    m1 = missions[0]["id"]
    m2 = missions[1]["id"]

    # Create assignment (INVITED)
    r = client.post("/api/v1/assignments", headers={"Authorization": f"Bearer {token}"}, json={"mission_id": m1, "user_id": user_id})
    assert r.status_code == 200
    aid = r.json()["id"]

    # Create invitation -> get token
    r = client.post("/api/v1/invitations", headers={"Authorization": f"Bearer {token}"}, json={"assignment_id": aid, "email":"alice@example.com"})
    assert r.status_code == 200
    inv_id = r.json()["id"]
    inv_tok = r.json()["token"]

    # Accept invitation (updates assignment to ACCEPTED)
    r = client.post(f"/api/v1/invitations/{inv_id}/accept", params={"token": inv_tok})
    assert r.status_code == 200

    # Try to accept another assignment overlapping -> create assignment for mission 2 and set ACCEPTED: should be allowed (different day) then conflict list empty
    r = client.post("/api/v1/assignments", headers={"Authorization": f"Bearer {token}"}, json={"mission_id": m2, "user_id": user_id})
    assert r.status_code == 200
    aid2 = r.json()["id"]
    r = client.post(f"/api/v1/assignments/{aid2}:status", headers={"Authorization": f"Bearer {token}"}, json={"status":"ACCEPTED"})
    assert r.status_code == 200

    # Conflicts for user -> none expected
    r = client.get(
        f"/api/v1/conflicts/user/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
    assert r.json()["items"] == []

    # Duplicate mission 1 and try to ACCEPT overlapping -> should 400 on status change
    r = client.post(f"/api/v1/missions/{m1}:duplicate", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    dup_id = r.json()["id"]
    r = client.post("/api/v1/assignments", headers={"Authorization": f"Bearer {token}"}, json={"mission_id": dup_id, "user_id": user_id})
    assert r.status_code == 200
    dup_aid = r.json()["id"]
    r = client.post(f"/api/v1/assignments/{dup_aid}:status", headers={"Authorization": f"Bearer {token}"}, json={"status":"ACCEPTED"})
    assert r.status_code == 400
