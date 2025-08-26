from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db

router = APIRouter(prefix="/api/v1/assignments", tags=["assignments"])


class AssignmentIn(BaseModel):
    mission_id: str
    user_id: str
    status: str = "INVITED"


class AssignmentOut(BaseModel):
    id: str
    mission_id: str
    user_id: str
    status: str


def _overlap(a_start: str, a_end: str, b_start: str, b_end: str) -> bool:
    return not (a_end <= b_start or b_end <= a_start)


def _has_conflict(db: Session, org_id: str, user_id: str, mission_id: str) -> bool:
    row = db.execute(text("SELECT starts_at, ends_at FROM missions WHERE id=:m AND org_id=:o"), {"m": mission_id, "o": org_id}).fetchone()
    if not row:
        return False
    start, end = row.starts_at, row.ends_at
    rows = db.execute(
        text("SELECT m.starts_at, m.ends_at FROM assignments a JOIN missions m ON a.mission_id=m.id WHERE m.org_id=:o AND a.user_id=:u AND a.status='ACCEPTED'"),
        {"o": org_id, "u": user_id},
    ).fetchall()
    return any(_overlap(start, end, r.starts_at, r.ends_at) for r in rows)
@router.post("", response_model=AssignmentOut)
def create_assignment(payload: AssignmentIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    row = db.execute(
        text("INSERT INTO assignments (id, mission_id, user_id, status, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :m, :u, :s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id, mission_id, user_id, status"),
        {"m": payload.mission_id, "u": payload.user_id, "s": payload.status},
    ).fetchone()
    assert row is not None
    db.commit()
    return dict(row._mapping)


class StatusIn(BaseModel):
    status: str


@router.post("/{aid}:status", response_model=AssignmentOut)
def set_status(aid: str, payload: StatusIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    # If moving to ACCEPTED, check conflicts
    if payload.status == "ACCEPTED":
        r = db.execute(text("SELECT mission_id, user_id FROM assignments WHERE id=:a"), {"a": aid}).fetchone()
        if not r:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="assignment introuvable")
        if _has_conflict(db, org_id, r.user_id, r.mission_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="conflit horaire utilisateur")
    row = db.execute(
        text("UPDATE assignments SET status=:s, updated_at=CURRENT_TIMESTAMP WHERE id=:a RETURNING id, mission_id, user_id, status"),
        {"s": payload.status, "a": aid},
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="assignment introuvable")
    db.commit()
    return dict(row._mapping)
