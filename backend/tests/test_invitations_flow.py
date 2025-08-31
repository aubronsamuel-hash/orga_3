from __future__ import annotations

import os
from datetime import datetime, timedelta
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

TEST_DB_PATH = Path("backend/test_invitations_flow.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"


def _cleanup() -> None:
    if TEST_DB_PATH.exists():
        try:
            TEST_DB_PATH.unlink(missing_ok=True)
        except PermissionError:
            pass


def _upgrade() -> None:
    os.environ["DB_URL"] = TEST_DB_URL
    os.environ["DATABASE_URL"] = TEST_DB_URL
    cfg = Config("backend/alembic.ini")
    command.upgrade(cfg, "head")


def _seed() -> None:
    eng = create_engine(TEST_DB_URL, future=True)
    now = datetime.utcnow()
    later = now + timedelta(hours=1)
    with eng.begin() as s:
        s.execute(text("INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('org1','Org',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        s.execute(text("INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) VALUES ('acc1','org1','a@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        s.execute(text("INSERT INTO users (id, org_id, account_id, first_name, last_name, employment_type, created_at, updated_at) VALUES ('u1','org1','acc1','Sam','A','Intermittent',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        s.execute(text("INSERT INTO projects (id, org_id, name, status, created_at, updated_at) VALUES ('p1','org1','Proj','DRAFT',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        s.execute(text("INSERT INTO missions (id, org_id, project_id, title, starts_at, ends_at, created_at, updated_at) VALUES ('m1','org1','p1','Bal',:s,:e,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"), {"s": now.isoformat(), "e": later.isoformat()})
        s.execute(text("INSERT INTO assignments (id, mission_id, user_id, status, created_at, updated_at) VALUES ('a1','m1','u1','INVITED',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
    eng.dispose()


def _client() -> TestClient:
    os.environ["DATABASE_URL"] = TEST_DB_URL
    from app.main import create_app
    from app import db

    app = create_app()
    db.Base.metadata.create_all(bind=db.engine)
    return TestClient(app)


def setup_function(_: object) -> None:
    _cleanup()
    _upgrade()
    _seed()


def teardown_function(_: object) -> None:
    _cleanup()


def test_invite_accept_flow() -> None:
    client = _client()
    resp = client.post("/api/v1/invitations", json={"assignment_id": "a1"})
    assert resp.status_code == 200
    token = resp.json()["token"]

    resp = client.get(f"/api/v1/invitations/verify?token={token}")
    assert resp.status_code == 200
    assert resp.json()["assignment_id"] == "a1"

    r = client.post("/api/v1/assignments/a1/accept", params={"token": token})
    assert r.status_code == 200
    assert r.json()["status"] == "ACCEPTED"


def test_invite_decline_reason() -> None:
    client = _client()
    token = client.post("/api/v1/invitations", json={"assignment_id": "a1"}).json()["token"]
    r = client.post(
        "/api/v1/assignments/a1/decline",
        params={"token": token},
        json={"reason": "not available"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "DECLINED"


def test_invite_token_revoked() -> None:
    client = _client()
    data = client.post("/api/v1/invitations", json={"assignment_id": "a1"}).json()
    inv_id, token = data["id"], data["token"]
    client.delete(f"/api/v1/invitations/{inv_id}")
    r = client.post("/api/v1/assignments/a1/accept", params={"token": token})
    assert r.status_code == 400
