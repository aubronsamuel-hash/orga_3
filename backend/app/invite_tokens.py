from __future__ import annotations
from datetime import datetime, timedelta, timezone
import time
import uuid
from typing import Any, Dict

import jwt

from .settings import settings


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def create_invite_token(invitation_id: str, org_id: str) -> str:
    exp = _now_utc() + timedelta(hours=int(settings.dict().get("invite_token_ttl_hours", 48)))
    payload: Dict[str, Any] = {
        "typ": "invite",
        "inv": invitation_id,
        "org": org_id,
        "iat": int(time.time()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_invite_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
