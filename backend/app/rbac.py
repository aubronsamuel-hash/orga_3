from __future__ import annotations

from enum import IntEnum
from typing import Any, Callable, Dict

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from .auth import get_current_account, get_db


class Role(IntEnum):
    tech = 10
    manager = 20
    admin = 30
    owner = 40


def _role_score(role_str: str) -> int:
    try:
        return Role[role_str].value
    except KeyError:
        return -1


def require_role(min_role: Role) -> Callable:
    """
    Dep FastAPI: exige membership dans l'org et un rôle >= min_role
    """

    def dep(
        current: Dict[str, Any] = Depends(get_current_account),
        db: Session = Depends(get_db),
    ) -> Dict[str, Any]:
        org_id = current["org_id"]
        acc_id = current["id"]
        row = db.execute(
            text(
                "SELECT role FROM org_memberships WHERE org_id=:o AND account_id=:a"
            ),
            {"o": org_id, "a": acc_id},
        ).fetchone()
        if not row:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="membre requis"
            )
        if _role_score(str(row.role)) < int(min_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="role insuffisant"
            )
        return {"org_id": org_id, "account_id": acc_id, "role": row.role}

    return dep


def require_org_scope(
    org_id: str = Path(...),
    current: Dict[str, Any] = Depends(get_current_account),
) -> Dict[str, Any]:
    """Dep: exige que l'org_id du path corresponde au claim org du token"""
    if current["org_id"] != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="org mismatch"
        )
    return {"org_id": org_id, "account_id": current["id"]}
