from __future__ import annotations

import os

from sqlalchemy import create_engine, text

from .utils import _client, _mk_account_and_members, _upgrade, TEST_DB_URL


def test_conflicts_overlap_same_day() -> None:
    os.environ["ENV"] = "dev"
    _upgrade(TEST_DB_URL)
    account_id, org_id = _mk_account_and_members(TEST_DB_URL)
    client = _client()
    eng = create_engine(TEST_DB_URL, future=True)

    r = client.post(
        "/api/v1/users", headers={"Authorization": "***"}, json={"name": "Max"}
    )
    user_id = r.json()["id"]

    with eng.begin() as c:
        m1 = c.execute(
            text(
                "INSERT INTO missions (id, org_id, title, starts_at, ends_at, created_at, updated_at) "
                "VALUES (lower(hex(randomblob(8))), :o, 'm1', :sa, :ea, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id"
            ),
            {"o": org_id, "sa": "2025-09-02T09:00:00Z", "ea": "2025-09-02T12:00:00Z"},
        ).scalar_one()
        m2 = c.execute(
            text(
                "INSERT INTO missions (id, org_id, title, starts_at, ends_at, created_at, updated_at) "
                "VALUES (lower(hex(randomblob(8))), :o, 'm2', :sa, :ea, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id"
            ),
            {"o": org_id, "sa": "2025-09-02T10:00:00Z", "ea": "2025-09-02T13:00:00Z"},
        ).scalar_one()
        for mid in [m1, m2]:
            c.execute(
                text(
                    "INSERT INTO assignments (id, mission_id, user_id, status, created_at, updated_at) "
                    "VALUES (lower(hex(randomblob(8))), :m, :u, 'ACCEPTED', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
                ),
                {"m": mid, "u": user_id},
            )

    r = client.get(f"/api/v1/conflicts/user/{user_id}")
    assert r.status_code == 200
    items = r.json()["items"]
    assert len(items) >= 1

