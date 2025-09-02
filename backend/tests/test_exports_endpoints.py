from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.api.v1 import exports as exports_api

client = TestClient(app)


def test_export_csv_ok(monkeypatch):
    def fake_compute(db, org_id, project_id, date_from, date_to):  # noqa: ARG001
        return [
            {
                "user_id": "u1",
                "user_name": "Alice",
                "month": "2025-08",
                "hours_planned": 10.0,
                "hours_confirmed": 8.0,
                "amount": 200.0,
            }
        ]

    monkeypatch.setattr(exports_api, "compute_monthly_totals", fake_compute)
    r = client.get(
        "/api/v1/exports/csv",
        params=dict(
            type="monthly-users",
            org_id="org1",
            date_from="2025-08-01",
            date_to="2025-08-31",
        ),
    )
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")


def test_export_pdf_type_ko():
    r = client.get(
        "/api/v1/exports/pdf",
        params=dict(
            type="unknown",
            org_id="org1",
            date_from="2025-08-01",
            date_to="2025-08-31",
        ),
    )
    assert r.status_code == 400
