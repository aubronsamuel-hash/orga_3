from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .auth import get_db
from .rbac import require_role, Role

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


class ProjectIn(BaseModel):
    name: str
    status: str = "DRAFT"


class ProjectOut(BaseModel):
    id: str
    name: str
    status: str


@router.post("", response_model=ProjectOut)
def create_project(payload: ProjectIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    row = db.execute(
        text(
            "INSERT INTO projects (id, org_id, name, status, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :o, :n, :s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id, name, status"
        ),
        {"o": org_id, "n": payload.name, "s": payload.status},
    ).fetchone()
    assert row is not None
    db.commit()
    return {"id": row.id, "name": row.name, "status": row.status}


@router.get("", response_model=List[ProjectOut])
def list_projects(current=Depends(require_role(Role.tech)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    rows = db.execute(
        text("SELECT id, name, status FROM projects WHERE org_id=:o ORDER BY created_at DESC"),
        {"o": org_id},
    ).fetchall()
    return [{"id": r.id, "name": r.name, "status": r.status} for r in rows]


@router.get("/{pid}", response_model=ProjectOut)
def get_project(pid: str, current=Depends(require_role(Role.tech)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    row = db.execute(
        text("SELECT id, name, status FROM projects WHERE id=:p AND org_id=:o"),
        {"p": pid, "o": org_id},
    ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project introuvable")
    return {"id": row.id, "name": row.name, "status": row.status}


@router.put("/{pid}", response_model=ProjectOut)
def update_project(pid: str, payload: ProjectIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    row = db.execute(
        text(
            "UPDATE projects SET name=:n, status=:s, updated_at=CURRENT_TIMESTAMP WHERE id=:p AND org_id=:o RETURNING id,name,status"
        ),
        {"n": payload.name, "s": payload.status, "p": pid, "o": org_id},
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project introuvable")
    return {"id": row.id, "name": row.name, "status": row.status}


@router.delete("/{pid}")
def delete_project(pid: str, current=Depends(require_role(Role.admin)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    res = db.execute(text("DELETE FROM projects WHERE id=:p AND org_id=:o"), {"p": pid, "o": org_id})
    db.commit()
    if res.rowcount == 0:  # type: ignore[attr-defined]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project introuvable")
    return {"status": "ok"}


class MissionBulkItem(BaseModel):
    start_at: str
    end_at: str
    role: str = "tech"


@router.post("/{pid}/missions:bulk_create")
def bulk_create_missions(pid: str, items: List[MissionBulkItem], current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    # verify project belongs to org
    if not db.execute(text("SELECT 1 FROM projects WHERE id=:p AND org_id=:o"), {"p": pid, "o": org_id}).fetchone():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project introuvable")
    for it in items:
        db.execute(
            text("INSERT INTO missions (id, org_id, project_id, title, starts_at, ends_at, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :o, :p, :r, :sa, :ea, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"),
            {"o": org_id, "p": pid, "sa": it.start_at, "ea": it.end_at, "r": it.role},
        )
    db.commit()
    return {"status": "ok", "created": len(items)}
