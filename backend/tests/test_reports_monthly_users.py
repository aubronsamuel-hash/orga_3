from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.api.v1 import reports as reports_api

client = TestClient(app)


def test_monthly_users_ok(monkeypatch):
    def fake_compute(db, org_id, project_id, date_from, date_to):  # noqa: ARG001
        return [
            {
                "user_id": "u1",
                "user_name": "Alice",
                "month": "2025-08",
                "hours_planned": 10.0,
                "hours_confirmed": 8.0,
                "amount": 200.0,
            },
            {
                "user_id": "u2",
                "user_name": "Bob",
                "month": "2025-08",
                "hours_planned": 12.0,
                "hours_confirmed": 12.0,
                "amount": 300.0,
            },
        ]

    monkeypatch.setattr(reports_api, "compute_monthly_totals", fake_compute)
    r = client.get(
        "/api/v1/reports/monthly-users",
        params=dict(org_id="org1", date_from="2025-08-01", date_to="2025-08-31"),
    )
    assert r.status_code == 200
    data = r.json()
    assert data["org_id"] == "org1"
    assert len(data["items"]) == 2
    assert data["items"][0]["user_name"] == "Alice"


def test_monthly_users_ko_bad_dates():
    r = client.get(
        "/api/v1/reports/monthly-users",
        params=dict(org_id="org1", date_from="2025-09-02", date_to="2025-08-01"),
    )
    assert r.status_code == 400
