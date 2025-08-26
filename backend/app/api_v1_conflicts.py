from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db

router = APIRouter(prefix="/api/v1/conflicts", tags=["conflicts"])


@router.get("/user/{uid}")
def conflicts_for_user(uid: str, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    rows = db.execute(
        text(
            """
SELECT a1.id AS a1, a2.id AS a2
FROM assignments a1
JOIN assignments a2 ON a1.id < a2.id AND a1.user_id=a2.user_id
JOIN missions m1 ON m1.id=a1.mission_id
JOIN missions m2 ON m2.id=a2.mission_id
WHERE m1.org_id=:o AND a1.user_id=:u AND a1.status='ACCEPTED' AND a2.status='ACCEPTED'
AND NOT (m1.ends_at <= m2.starts_at OR m2.ends_at <= m1.starts_at)
"""
        ),
        {"o": org_id, "u": uid},
    ).fetchall()
    return {"conflicts": [{"a1": r.a1, "a2": r.a2} for r in rows]}
