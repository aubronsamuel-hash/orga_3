from __future__ import annotations

import os
from datetime import datetime, timezone

from .utils import _client, _mk_account_and_members, _upgrade, TEST_DB_URL


def test_availability_flow_ok() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)
    _mk_account_and_members(TEST_DB_URL)
    client = _client()

    # Create user
    r = client.post(
        "/api/v1/users", headers={"Authorization": "***"}, json={"name": "Eve"}
    )
    assert r.status_code == 200
    user_id = r.json()["id"]

    # Upsert profile
    r = client.put(
        f"/api/v1/users/{user_id}/profile",
        headers={"Authorization": "***"},
        json={
            "skills": ["son", "lumiere"],
            "tags": ["bobino"],
            "employment_type": "INTERMITTENT",
            "rate_profile": {"jour": 250.0},
        },
    )
    assert r.status_code == 200
    assert r.json()["user_id"] == user_id

    # Request availability
    start = datetime(2025, 9, 3, 9, 0, 0, tzinfo=timezone.utc).isoformat()
    end = datetime(2025, 9, 3, 18, 0, 0, tzinfo=timezone.utc).isoformat()
    r = client.post(
        "/api/v1/availabilities",
        headers={"Authorization": "***"},
        json={
            "user_id": user_id,
            "start_at": start,
            "end_at": end,
            "note": "dispo",
        },
    )
    assert r.status_code == 200
    avail_id = r.json()["id"]

    # Approve
    r = client.post(
        f"/api/v1/availabilities/{avail_id}:approve",
        headers={"Authorization": "***"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "APPROVED"

    # Calendar
    r = client.get(
        f"/api/v1/users/{user_id}/calendar?from=2025-09-01T00:00:00Z&to=2025-09-30T00:00:00Z",
        headers={"Authorization": "***"},
    )
    assert r.status_code == 200
    assert len(r.json()) == 1
