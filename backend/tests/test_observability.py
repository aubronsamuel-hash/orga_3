from __future__ import annotations


import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

TEST_DB_PATH = Path("backend/test_obs.db").resolve()
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"


def _upgrade(url: str) -> None:
    os.environ["DB_URL"] = url
    os.environ["DATABASE_URL"] = url
    cfg = Config("backend/alembic.ini")
    command.upgrade(cfg, "head")


def _client():
    from backend.app.main import create_app

    app = create_app()
    return TestClient(app)


def test_metrics_endpoint_exposes_metrics() -> None:
    os.environ["ENV"] = "dev"
    os.environ["METRICS_ENABLED"] = "true"
    client = _client()
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "app_request_duration_seconds" in r.text


def test_probes_livez_readyz_ok() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)
    client = _client()

    r1 = client.get("/livez")
    assert r1.status_code == 200
    assert r1.json()["status"] == "live"

    r2 = client.get("/readyz")
    assert r2.status_code == 200
    assert r2.json()["status"]["ok"] is True


def test_logs_json_have_ids() -> None:
    os.environ["ENV"] = "dev"
    client = _client()
    r = client.get("/healthz", headers={"X-Request-ID": "rid123"})
    assert r.status_code == 200
    assert r.headers["X-Request-ID"] == "rid123"
