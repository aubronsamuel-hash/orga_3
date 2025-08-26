from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db

router = APIRouter(prefix="/api/v1/rates", tags=["rates"])


@router.post("/user/{uid}")
def set_user_rate(uid: str, daily_eur: float, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    db.execute(
        text("UPDATE users SET rate_profile=:r, updated_at=CURRENT_TIMESTAMP WHERE id=:u AND org_id=:o"),
        {"r": f"DAILY:{daily_eur}", "u": uid, "o": org_id},
    )
    db.commit()
    return {"status": "ok"}


@router.get("/user/{uid}")
def get_user_rate(uid: str, current=Depends(require_role(Role.tech)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    r = db.execute(text("SELECT rate_profile FROM users WHERE id=:u AND org_id=:o"), {"u": uid, "o": org_id}).fetchone()
    return {"rate_profile": r.rate_profile if r else None}
