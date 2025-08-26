from __future__ import annotations

import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

TEST_DB_PATH = Path("backend/test_rbac.db").resolve()
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


def _mk_token(account_id: str, org_id: str) -> str:
    # import tardif apres alembic
    from app.auth import create_access_token

    return create_access_token(account_id, org_id)


def _client() -> TestClient:
    from app.main import create_app

    app = create_app()
    return TestClient(app)


def test_rbac_enforcement_ok_and_ko() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)

    eng = create_engine(TEST_DB_URL, future=True)
    with eng.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO orgs (id, name, created_at, updated_at) "
                "VALUES ('o1','Org1',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        conn.execute(
            text(
                "INSERT INTO orgs (id, name, created_at, updated_at) "
                "VALUES ('o2','Org2',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        conn.execute(
            text(
                "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) "
                "VALUES ('a1','o1','a1@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        conn.execute(
            text(
                "INSERT INTO accounts (id, org_id, email, is_active, created_at, updated_at) "
                "VALUES ('a2','o1','a2@example.com',1,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        conn.execute(
            text(
                "INSERT INTO org_memberships (id, org_id, account_id, role, created_at, updated_at) "
                "VALUES ('m1','o1','a1','manager',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )
        conn.execute(
            text(
                "INSERT INTO org_memberships (id, org_id, account_id, role, created_at, updated_at) "
                "VALUES ('m2','o1','a2','tech',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)"
            )
        )

    t_mgr = _mk_token("a1", "o1")
    t_tech = _mk_token("a2", "o1")

    client = _client()

    # any: membre requis
    r = client.get(
        "/api/v1/rbac_demo/any", headers={"Authorization": f"Bearer {t_mgr}"}
    )
    assert r.status_code == 200
    r = client.get(
        "/api/v1/rbac_demo/any", headers={"Authorization": f"Bearer {t_tech}"}
    )
    assert r.status_code == 200

    # manager+: tech doit echouer
    r = client.get(
        "/api/v1/rbac_demo/manager",
        headers={"Authorization": f"Bearer {t_mgr}"},
    )
    assert r.status_code == 200
    r = client.get(
        "/api/v1/rbac_demo/manager",
        headers={"Authorization": f"Bearer {t_tech}"},
    )
    assert r.status_code == 403

    # admin+: manager echoue
    r = client.get(
        "/api/v1/rbac_demo/admin", headers={"Authorization": f"Bearer {t_mgr}"}
    )
    assert r.status_code == 403

    # scope org: token o1, path o1 OK / o2 KO
    r = client.get(
        "/api/v1/rbac_demo/scoped/o1", headers={"Authorization": f"Bearer {t_mgr}"}
    )
    assert r.status_code == 200
    r = client.get(
        "/api/v1/rbac_demo/scoped/o2", headers={"Authorization": f"Bearer {t_mgr}"}
    )
    assert r.status_code == 403
