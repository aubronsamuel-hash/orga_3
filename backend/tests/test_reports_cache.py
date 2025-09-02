from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services import reports as reports_service

client = TestClient(app)


def test_reports_cache_hits(monkeypatch):
    calls = {"n": 0}

    def fake_compute(db, org_id, project_id, date_from, date_to):
        calls["n"] += 1
        return [
            {
                "user_id": "u",
                "user_name": "Test",
                "month": "2025-08",
                "hours_planned": 1.0,
                "hours_confirmed": 1.0,
                "amount": 10.0,
            }
        ]

    monkeypatch.setattr(reports_service, "compute_monthly_totals", fake_compute)
    r1 = client.get(
        "/api/v1/reports/monthly-users",
        params=dict(org_id="o", date_from="2025-08-01", date_to="2025-08-31"),
    )
    assert r1.status_code == 200
    r2 = client.get(
        "/api/v1/reports/monthly-users",
        params=dict(org_id="o", date_from="2025-08-01", date_to="2025-08-31"),
    )
    assert r2.status_code == 200
    assert calls["n"] == 1

