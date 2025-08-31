from __future__ import annotations
import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from ..core.config import settings


_DEF_ALGO = "HS256"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def sign_invite_token(assignment_id: str) -> tuple[str, str]:
    """Sign a token for an assignment.

    Returns the token and the sha256 hash of the jti for storage.
    """
    jti = str(uuid.uuid4())
    exp = _now() + timedelta(seconds=settings.INVITES_TTL_SECONDS)
    payload = {"sub": assignment_id, "jti": jti, "exp": exp}
    token = jwt.encode(payload, settings.INVITES_SECRET, algorithm=_DEF_ALGO)
    token_hash = hashlib.sha256(jti.encode()).hexdigest()
    return token, token_hash


def verify_invite_token(token: str) -> Dict[str, Any]:
    """Verify token signature and expiration."""
    return jwt.decode(token, settings.INVITES_SECRET, algorithms=[_DEF_ALGO])
