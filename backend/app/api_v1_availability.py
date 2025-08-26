from __future__ import annotations
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db

router = APIRouter(prefix="/api/v1/availability", tags=["availability"])


class AvailIn(BaseModel):
    user_id: str
    start_at: str
    end_at: str


@router.post("")
def create_availability(payload: AvailIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    db.execute(
        text("INSERT INTO availability (id, org_id, user_id, start_at, end_at, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :o, :u, :s, :e, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"),
        {"o": org_id, "u": payload.user_id, "s": payload.start_at, "e": payload.end_at},
    )
    db.commit()
    return {"status": "ok"}
