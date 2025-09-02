import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

TEST_DB_PATH = Path("backend/test_cache.db").resolve()
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
    _cleanup()
    os.environ["DB_URL"] = url
    os.environ["DATABASE_URL"] = url
    os.environ["REDIS_URL"] = "fakeredis://"
    cfg = Config("backend/alembic.ini")
    command.upgrade(cfg, "head")


def _client() -> TestClient:
    from backend.app.main import create_app

    app = create_app()
    return TestClient(app)


def test_projects_cache_hit_miss_and_invalidation() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)

    eng = create_engine(TEST_DB_URL, future=True)
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
    from backend.app.auth import create_access_token

    token = create_access_token("a1", "o1")
    client = _client()

    r1 = client.get("/api/v1/projects", headers={"Authorization": f"Bearer {token}"})
    assert r1.status_code == 200
    assert r1.headers.get("X-Cache") == "MISS"

    r2 = client.get("/api/v1/projects", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.headers.get("X-Cache") == "HIT"

    r3 = client.post(
        "/api/v1/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "P1", "status": "ACTIVE"},
    )
    assert r3.status_code == 200
    r4 = client.get("/api/v1/projects", headers={"Authorization": f"Bearer {token}"})
    assert r4.status_code == 200
    assert r4.headers.get("X-Cache") == "MISS"


def test_missions_cache_hit_miss() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)

    eng = create_engine(TEST_DB_URL, future=True)
    with eng.begin() as c:
        # Utiliser un jeu distinct pour eviter les collisions avec le test precedent
        c.execute(
            text(
                "INSERT INTO orgs (id, name, created_at, updated_at) VALUES ('o2','Org2',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        c.execute(
            text(
                "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) VALUES ('a2','o2','mgr2@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        c.execute(
            text(
                "INSERT INTO org_memberships (id, org_id, account_id, role, created_at, updated_at) VALUES ('m2','o2','a2','manager',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
    from backend.app.auth import create_access_token

    token = create_access_token("a2", "o2")
    client = _client()

    r1 = client.get("/api/v1/missions", headers={"Authorization": f"Bearer {token}"})
    assert r1.status_code == 200
    assert r1.headers.get("X-Cache") == "MISS"

    r2 = client.get("/api/v1/missions", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200
    assert r2.headers.get("X-Cache") == "HIT"
