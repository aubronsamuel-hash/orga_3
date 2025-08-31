import hashlib
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from ..core.config import settings
from ..models import Assignment, Invitation
from ..enums import AssignmentStatus
from .tokens import sign_invite_token, verify_invite_token


def _now() -> datetime:
    return datetime.utcnow()


def create_invitation(db: Session, assignment_id: str) -> tuple[Invitation, str]:
    token, token_hash = sign_invite_token(assignment_id)
    expires = _now() + timedelta(seconds=settings.INVITES_TTL_SECONDS)
    inv = Invitation(
        assignment_id=assignment_id,
        token_hash=token_hash,
        expires_at=expires,
        created_at=_now(),
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv, token


def revoke_invitation(db: Session, invitation: Invitation) -> None:
    invitation.revoked_at = _now()
    db.add(invitation)
    db.commit()


def get_invitation_by_token(db: Session, token: str) -> Optional[Invitation]:
    try:
        data = verify_invite_token(token)
    except Exception:
        return None
    token_hash = data.get("jti")
    if token_hash is None:
        return None
    token_hash = hashlib.sha256(token_hash.encode()).hexdigest()
    inv = db.query(Invitation).filter_by(token_hash=token_hash).first()
    if not inv:
        return None
    if inv.revoked_at is not None:
        return None
    if inv.expires_at <= _now():
        return None
    return inv


class InvitationNotFound(Exception):
    pass


class InvalidInvitationToken(Exception):
    pass


def accept_invitation(db: Session, invitation_id: str, token: str) -> Invitation:
    inv = get_invitation_by_token(db, token)
    if not inv or inv.id != invitation_id:
        raise InvalidInvitationToken()
    asg = db.query(Assignment).filter_by(id=inv.assignment_id).first()
    if not asg:
        raise InvitationNotFound()
    if asg.status != AssignmentStatus.ACCEPTED.value:
        asg.status = AssignmentStatus.ACCEPTED.value
        asg.updated_at = _now()
        inv.used_at = _now()
        db.add(asg)
        db.add(inv)
        db.commit()
        db.refresh(inv)
    return inv
