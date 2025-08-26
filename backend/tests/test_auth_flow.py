from __future__ import annotations
import os
os.environ["ENV"] = "dev"
from pathlib import Path

TEST_DB_PATH = Path("backend/test_auth.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"
os.environ["DATABASE_URL"] = TEST_DB_URL

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from app.main import create_app
from sqlalchemy import create_engine, text

from app.auth import hash_password


def _upgrade(url: str) -> None:
    os.environ["DB_URL"] = url
    os.environ["DATABASE_URL"] = url
    cfg = Config("backend/alembic.ini")
    command.upgrade(cfg, "head")


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


def test_login_refresh_me_logout_flow() -> None:
    _upgrade(TEST_DB_URL)
    client = TestClient(create_app())

    eng = create_engine(TEST_DB_URL, future=True)
    with eng.begin() as conn:
        conn.execute(text("INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('o1','Org',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        conn.execute(
            text(
                "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at, password_hash) VALUES ('a1','o1','sam@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,:ph)"
            ),
            {"ph": hash_password("secret")},
        )

    # login
    r = client.post("/api/v1/auth/login", json={"email": "sam@example.com", "password": "secret"})
    assert r.status_code == 200
    access = r.json().get("access_token")
    assert access
    assert "refresh_token" in r.cookies

    # me with access
    r2 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access}"})
    assert r2.status_code == 200
    assert r2.json()["email"] == "sam@example.com"

    # refresh to get new access
    r3 = client.post("/api/v1/auth/refresh")
    assert r3.status_code == 200
    assert r3.json().get("access_token")

    # logout clears cookie
    r4 = client.post("/api/v1/auth/logout")
    assert r4.status_code == 200
    assert r4.json()["status"] == "ok"
