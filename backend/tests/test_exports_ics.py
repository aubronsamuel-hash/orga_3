from __future__ import annotations

from datetime import datetime, timezone, timedelta

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services import ics as ics_service

client = TestClient(app)


def _fake_loader(db, project_id, date_from, date_to):
    base = datetime(2025, 8, 20, 12, 0, tzinfo=timezone.utc)
    return [
        {
            "uid": "evt1",
            "dtstart": base,
            "dtend": base + timedelta(hours=2),
            "summary": "Repetition",
            "description": "Salle A",
        },
        {
            "uid": "evt2",
            "dtstart": base + timedelta(days=1),
            "dtend": base + timedelta(days=1, hours=3),
            "summary": "Show",
            "description": "Scene",
        },
    ]


def test_export_ics_ok(monkeypatch):
    monkeypatch.setattr(ics_service, "default_loader", _fake_loader)
    r = client.get(
        "/api/v1/exports/ics",
        params=dict(project_id="p1", date_from="2025-08-01", date_to="2025-08-31"),
    )
    assert r.status_code == 200
    body = r.text
    assert "BEGIN:VCALENDAR" in body
    assert "SUMMARY:Show" in body
    assert "UID:evt1" in body


def test_export_ics_ko_bad_dates():
    r = client.get(
        "/api/v1/exports/ics",
        params=dict(project_id="p1", date_from="2025-09-02", date_to="2025-08-01"),
    )
    assert r.status_code == 400

