from __future__ import annotations

import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .db import SessionLocal
from .settings import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return pwd_ctx.verify(password, password_hash)
    except Exception:
        return False

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def create_access_token(sub: str, org_id: Optional[str]) -> str:
    exp = _now_utc() + timedelta(minutes=settings.access_token_minutes)
    payload = {
        "sub": sub,
        "org": org_id,
        "typ": "access",
        "iat": int(time.time()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(sub: str, org_id: Optional[str]) -> str:
    exp = _now_utc() + timedelta(days=settings.refresh_token_days)
    payload = {
        "sub": sub,
        "org": org_id,
        "typ": "refresh",
        "iat": int(time.time()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

def create_reset_token(email: str) -> str:
    exp = _now_utc() + timedelta(hours=1)
    payload = {
        "email": email,
        "typ": "reset",
        "iat": int(time.time()),
        "exp": int(exp.timestamp()),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expire")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalide")

def get_db() -> Session:
    return SessionLocal()

def get_current_account(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    request: Request = None,  # type: ignore[assignment]
    db: Session = Depends(get_db),
):
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="auth manquante")
    token = creds.credentials
    data = decode_token(token)
    if data.get("typ") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="mauvais type de token")
    sub = data.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="sub absent")
    # Lookup rapide
    from sqlalchemy import text

    row = db.execute(text("SELECT id,email,org_id FROM accounts WHERE id=:id"), {"id": sub}).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="compte inconnu")
    return {"id": row.id, "email": row.email, "org_id": row.org_id}

def set_refresh_cookie(response, refresh_token: str) -> None:
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # dev; activer en prod derriere TLS
        samesite="lax",
        path="/api/v1/auth",
        max_age=int(timedelta(days=settings.refresh_token_days).total_seconds()),
    )

def clear_refresh_cookie(response) -> None:
    response.delete_cookie(key="refresh_token", path="/api/v1/auth")
