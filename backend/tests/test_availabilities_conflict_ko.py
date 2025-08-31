from __future__ import annotations

import os

from tests.utils import _client, _mk_account_and_members, _upgrade, TEST_DB_URL


def test_conflict_on_overlap_ko() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)
    _mk_account_and_members(TEST_DB_URL)
    client = _client()

    r = client.post(
        "/api/v1/users", headers={"Authorization": "***"}, json={"name": "Max"}
    )
    user_id = r.json()["id"]

    # first slot approve
    r = client.post(
        "/api/v1/availabilities",
        headers={"Authorization": "***"},
        json={
            "user_id": user_id,
            "start_at": "2025-09-02T09:00:00Z",
            "end_at": "2025-09-02T12:00:00Z",
        },
    )
    aid = r.json()["id"]
    r = client.post(f"/api/v1/availabilities/{aid}:approve", headers={"Authorization": "***"})
    assert r.status_code == 200

    # overlapping second -> approve must 409
    r = client.post(
        "/api/v1/availabilities",
        headers={"Authorization": "***"},
        json={
            "user_id": user_id,
            "start_at": "2025-09-02T11:00:00Z",
            "end_at": "2025-09-02T13:00:00Z",
        },
    )
    bid = r.json()["id"]
    r = client.post(
        f"/api/v1/availabilities/{bid}:approve", headers={"Authorization": "***"}
    )
    assert r.status_code == 409
