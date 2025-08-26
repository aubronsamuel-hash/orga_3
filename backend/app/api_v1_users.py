from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])


class UserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: str
    name: str


@router.post("", response_model=UserOut)
def create_user(payload: UserIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    row = db.execute(
        text("INSERT INTO users (id, org_id, first_name, last_name, employment_type, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :o, :n, :ln, :et, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id, first_name AS name"),
        {"o": org_id, "n": payload.name, "ln": "", "et": "CDI"},
    ).fetchone()
    assert row is not None
    db.commit()
    return dict(row._mapping)


@router.get("", response_model=List[UserOut])
def list_users(q: str | None = Query(default=None), current=Depends(require_role(Role.tech)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    if q:
        rows = db.execute(
            text("SELECT id, first_name AS name FROM users WHERE org_id=:o AND first_name LIKE :q ORDER BY first_name"),
            {"o": org_id, "q": f"%{q}%"},
        ).fetchall()
    else:
        rows = db.execute(
            text("SELECT id, first_name AS name FROM users WHERE org_id=:o ORDER BY first_name"),
            {"o": org_id},
        ).fetchall()
    return [dict(r._mapping) for r in rows]
