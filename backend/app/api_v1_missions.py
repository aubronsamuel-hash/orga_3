from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db

router = APIRouter(prefix="/api/v1/missions", tags=["missions"])


class MissionIn(BaseModel):
    project_id: str | None = None
    start_at: str
    end_at: str
    role: str = "tech"


class MissionOut(BaseModel):
    id: str
    project_id: str | None
    start_at: str
    end_at: str
    role: str


@router.post("", response_model=MissionOut)
def create_mission(payload: MissionIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    row = db.execute(
        text(
            "INSERT INTO missions (id, org_id, project_id, title, starts_at, ends_at, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :o, :p, :t, :sa, :ea, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id, project_id, starts_at, ends_at, title"
        ),
        {"o": org_id, "p": payload.project_id, "t": payload.role, "sa": payload.start_at, "ea": payload.end_at},
    ).fetchone()
    assert row is not None
    db.commit()
    return dict(row._mapping)


@router.get("", response_model=List[MissionOut])
def list_missions(current=Depends(require_role(Role.tech)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    rows = db.execute(
        text("SELECT id, project_id, starts_at, ends_at, title FROM missions WHERE org_id=:o ORDER BY starts_at"),
        {"o": org_id},
    ).fetchall()
    return [{"id": r.id, "project_id": r.project_id, "start_at": r.starts_at, "end_at": r.ends_at, "role": r.title} for r in rows]


@router.post("/{mid}:duplicate", response_model=MissionOut)
def duplicate_mission(mid: str, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    src = db.execute(
        text("SELECT project_id, starts_at, ends_at, title FROM missions WHERE id=:m AND org_id=:o"),
        {"m": mid, "o": org_id},
    ).fetchone()
    if not src:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mission introuvable")
    row = db.execute(
        text(
            "INSERT INTO missions (id, org_id, project_id, title, starts_at, ends_at, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :o, :p, :t, :sa, :ea, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id, project_id, starts_at, ends_at, title"
        ),
        {"o": org_id, "p": src.project_id, "t": src.title, "sa": src.starts_at, "ea": src.ends_at},
    ).fetchone()
    assert row is not None
    db.commit()
    return {"id": row.id, "project_id": row.project_id, "start_at": row.starts_at, "end_at": row.ends_at, "role": row.title}
