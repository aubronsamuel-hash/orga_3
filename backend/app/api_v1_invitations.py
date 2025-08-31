from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth import get_db
from .models import Assignment, Invitation
from .services import invitations as inv_service

router = APIRouter(prefix="/api/v1/invitations", tags=["invitations"])


class InvitationCreate(BaseModel):
    assignment_id: str


class InvitationOut(BaseModel):
    id: str
    token: str
    expires_at: datetime


@router.post("", response_model=InvitationOut)
def create_invitation(payload: InvitationCreate, db: Session = Depends(get_db)):
    inv, token = inv_service.create_invitation(db, payload.assignment_id)
    return {"id": inv.id, "token": token, "expires_at": inv.expires_at}


@router.delete("/{invitation_id}")
def revoke_invitation(invitation_id: str, db: Session = Depends(get_db)):
    inv = db.query(Invitation).filter_by(id=invitation_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="invitation not found")
    inv_service.revoke_invitation(db, inv)
    return {"status": "ok"}


@router.get("/verify")
def verify_invitation(token: str = Query(...), db: Session = Depends(get_db)):
    inv = inv_service.get_invitation_by_token(db, token)
    if not inv:
        raise HTTPException(status_code=400, detail="invalid token")
    asg = db.query(Assignment).filter_by(id=inv.assignment_id).first()
    if not asg:
        raise HTTPException(status_code=404, detail="assignment not found")
    return {"assignment_id": asg.id, "status": asg.status, "expires_at": inv.expires_at}
