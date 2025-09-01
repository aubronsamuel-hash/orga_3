from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import text
from sqlalchemy.engine import RowMapping
from sqlalchemy.orm import Session

from app.schemas.conflicts import ConflictItem, ConflictList


def _normalize_iso_utc(s: str) -> datetime:
    s2 = s.strip().replace(" ", "T")
    if s2.endswith("Z"):
        s2 = s2[:-1] + "+00:00"
    return datetime.fromisoformat(s2)


def _overlap(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    return (a_start < b_end) and (b_start < a_end)


def list_user_conflicts(db: Session, user_id: str) -> ConflictList:
    # Lire TEXT + parser nous-memes (support du 'Z')
    sql = text(
        """
        SELECT
            a.mission_id AS mission_id,
            CAST(m.starts_at AS TEXT) AS starts_at,
            CAST(m.ends_at   AS TEXT) AS ends_at
        FROM assignments a
        JOIN missions m ON m.id = a.mission_id
        WHERE a.user_id = :uid AND a.status = 'ACCEPTED'
        ORDER BY m.starts_at ASC
        """
    )
    # .mappings() -> MappingResult[RowMapping]; .all() -> list[RowMapping]
    rows: List[RowMapping] = list(db.execute(sql, {"uid": user_id}).mappings().all())

    # Parse + detection des chevauchements O(n^2) (OK pour nos volumes de tests)
    parsed = [
        (
            r["mission_id"],
            _normalize_iso_utc(r["starts_at"]),
            _normalize_iso_utc(r["ends_at"]),
        )
        for r in rows
    ]

    items: List[ConflictItem] = []
    for i in range(len(parsed)):
        mid_a, sa, ea = parsed[i]
        for j in range(i + 1, len(parsed)):
            mid_b, sb, eb = parsed[j]
            if _overlap(sa, ea, sb, eb):
                items.append(
                    ConflictItem(
                        user_id=user_id,
                        mission_id=mid_a,
                        with_mission_id=mid_b,
                        starts_at=max(sa, sb).isoformat(),
                        ends_at=min(ea, eb).isoformat(),
                    )
                )

    return ConflictList(user_id=user_id, items=items)

