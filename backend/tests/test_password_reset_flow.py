from __future__ import annotations
import os
os.environ["ENV"] = "dev"
from pathlib import Path

TEST_DB_PATH = Path("backend/test_reset.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"
os.environ["DATABASE_URL"] = TEST_DB_URL

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from app.main import create_app
from sqlalchemy import create_engine, text

from app.auth import verify_password


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


def test_password_reset_dev_flow() -> None:
    _upgrade(TEST_DB_URL)
    client = TestClient(create_app())

    eng = create_engine(TEST_DB_URL, future=True)
    with eng.begin() as conn:
        conn.execute(text("INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('o1','Org',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"))
        conn.execute(
            text("INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at, password_hash) VALUES ('a1','o1','user@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP,'$2b$12$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')")
        )

    # request reset (in dev returns token)
    r = client.post("/api/v1/auth/reset/request", json={"email": "user@example.com"})
    assert r.status_code == 200
    tok = r.json().get("reset_token")
    assert tok, "en dev, le token doit etre renvoye"

    # confirm reset
    r2 = client.post("/api/v1/auth/reset/confirm", json={"token": tok, "new_password": "newpass123"})
    assert r2.status_code == 200

    # verify password actually changed
    with eng.connect() as conn:
        ph = conn.execute(text("SELECT password_hash FROM accounts WHERE email='user@example.com'"))
        ph = ph.scalar_one()
        assert verify_password("newpass123", ph)
