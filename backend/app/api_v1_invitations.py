from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from sqlalchemy.orm import Session

from .rbac import require_role, Role
from .auth import get_db
from .invite_tokens import create_invite_token, decode_invite_token

router = APIRouter(prefix="/api/v1/invitations", tags=["invitations"])


class InvitationIn(BaseModel):
    assignment_id: str
    email: EmailStr


@router.post("")
def create_invitation(payload: InvitationIn, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    a = db.execute(text("SELECT mission_id, user_id FROM assignments WHERE id=:a"), {"a": payload.assignment_id}).fetchone()
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="assignment introuvable")
    inv = db.execute(
        text("INSERT INTO invitations (id, org_id, mission_id, user_id, token, created_at, updated_at) VALUES (lower(hex(randomblob(8))), :o, :m, :u, '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING id"),
        {"o": org_id, "m": a.mission_id, "u": a.user_id},
    ).fetchone()
    assert inv is not None
    token = create_invite_token(inv.id, org_id)
    db.execute(text("UPDATE invitations SET token=:t WHERE id=:i"), {"t": token, "i": inv.id})
    db.commit()
    return {"id": inv.id, "token": token}


@router.post("/{iid}:revoke")
def revoke_invitation(iid: str, current=Depends(require_role(Role.manager)), db: Session = Depends(get_db)):
    org_id = current["org_id"]
    res = db.execute(text("DELETE FROM invitations WHERE id=:i AND org_id=:o"), {"i": iid, "o": org_id})
    db.commit()
    if res.rowcount == 0:  # type: ignore[attr-defined]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invitation introuvable")
    return {"status": "ok"}


@router.post("/{iid}/accept")
def accept_invitation(iid: str, token: str = Query(...), db: Session = Depends(get_db)):
    data = decode_invite_token(token)
    if data.get("typ") != "invite" or data.get("inv") != iid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token invalide")
    org_id = data.get("org")
    r = db.execute(text("SELECT mission_id, user_id FROM invitations WHERE id=:i AND org_id=:o"), {"i": iid, "o": org_id}).fetchone()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invitation introuvable")
    db.execute(text("UPDATE assignments SET status='ACCEPTED', updated_at=CURRENT_TIMESTAMP WHERE mission_id=:m AND user_id=:u"), {"m": r.mission_id, "u": r.user_id})
    db.commit()
    return {"status": "ok", "assignment_id": None, "new_status": "ACCEPTED"}


@router.post("/{iid}/decline")
def decline_invitation(iid: str, token: str = Query(...), db: Session = Depends(get_db)):
    data = decode_invite_token(token)
    if data.get("typ") != "invite" or data.get("inv") != iid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token invalide")
    org_id = data.get("org")
    r = db.execute(text("SELECT mission_id, user_id FROM invitations WHERE id=:i AND org_id=:o"), {"i": iid, "o": org_id}).fetchone()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invitation introuvable")
    db.execute(text("UPDATE assignments SET status='DECLINED', updated_at=CURRENT_TIMESTAMP WHERE mission_id=:m AND user_id=:u"), {"m": r.mission_id, "u": r.user_id})
    db.commit()
    return {"status": "ok", "assignment_id": None, "new_status": "DECLINED"}
