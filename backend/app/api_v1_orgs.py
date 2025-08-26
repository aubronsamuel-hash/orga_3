from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db

router = APIRouter(prefix="/api/v1/orgs", tags=["orgs"])


@router.get("/members")
def list_members(current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    rows = db.execute(
        text("SELECT account_id, role FROM org_memberships WHERE org_id=:o ORDER BY role DESC"),
        {"o": org_id},
    ).fetchall()
    return {"members": [{"account_id": r.account_id, "role": r.role} for r in rows]}
