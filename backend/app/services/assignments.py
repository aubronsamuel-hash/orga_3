from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from ..enums import AssignmentStatus
from ..models import Assignment
from .invitations import get_invitation_by_token


def _now() -> datetime:
    return datetime.utcnow()


def accept_assignment(db: Session, assignment_id: str, token: Optional[str] = None) -> Optional[Assignment]:
    inv = None
    if token:
        inv = get_invitation_by_token(db, token)
        if not inv or inv.assignment_id != assignment_id:
            raise ValueError("invalid token")
    asg = db.query(Assignment).filter_by(id=assignment_id).first()
    if not asg:
        return None
    asg.status = AssignmentStatus.ACCEPTED.value
    asg.updated_at = _now()
    if inv:
        inv.used_at = _now()
    db.commit()
    db.refresh(asg)
    return asg


def decline_assignment(
    db: Session,
    assignment_id: str,
    token: Optional[str] = None,
    reason: Optional[str] = None,
) -> Optional[Assignment]:
    inv = None
    if token:
        inv = get_invitation_by_token(db, token)
        if not inv or inv.assignment_id != assignment_id:
            raise ValueError("invalid token")
    asg = db.query(Assignment).filter_by(id=assignment_id).first()
    if not asg:
        return None
    asg.status = AssignmentStatus.DECLINED.value
    asg.updated_at = _now()
    if reason and hasattr(asg, "note"):
        asg.note = reason
    if inv:
        inv.used_at = _now()
    db.commit()
    db.refresh(asg)
    return asg
