from __future__ import annotations

from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import Assignment, Mission
from app.schemas.conflicts import ConflictItem, ConflictList


def _overlap(a_start, a_end, b_start, b_end) -> bool:
    return (a_start < b_end) and (b_start < a_end)


def list_user_conflicts(db: Session, user_id: str) -> ConflictList:
    q = (
        select(Assignment.mission_id, Mission.starts_at, Mission.ends_at)
        .join(Mission, Mission.id == Assignment.mission_id)
        .where(and_(Assignment.user_id == user_id, Assignment.status == "ACCEPTED"))
        .order_by(Mission.starts_at.asc())
    )
    rows = db.execute(q).all()
    items: List[ConflictItem] = []
    for i in range(len(rows)):
        a = rows[i]
        for j in range(i + 1, len(rows)):
            b = rows[j]
            if _overlap(a.starts_at, a.ends_at, b.starts_at, b.ends_at):
                items.append(
                    ConflictItem(
                        user_id=user_id,
                        mission_id=a.mission_id,
                        with_mission_id=b.mission_id,
                        starts_at=str(max(a.starts_at, b.starts_at)),
                        ends_at=str(min(a.ends_at, b.ends_at)),
                    )
                )
    return ConflictList(user_id=user_id, items=items)

