from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import text
from sqlalchemy.orm import Session

from .auth import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
    get_current_account,
    get_db,
    hash_password,
    set_refresh_cookie,
    clear_refresh_cookie,
    verify_password,
)
from .settings import settings

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ResetRequestIn(BaseModel):
    email: EmailStr


class ResetConfirmIn(BaseModel):
    token: str
    new_password: str


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    # lookup account
    row = db.execute(
        text("SELECT id, org_id, email, password_hash, is_active FROM accounts WHERE email=:e"),
        {"e": payload.email},
    ).fetchone()
    if not row or not row.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="identifiants invalides")
    if not row.password_hash or not verify_password(payload.password, row.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="identifiants invalides")
    acc_id = row.id
    access = create_access_token(acc_id, row.org_id)
    refresh = create_refresh_token(acc_id, row.org_id)
    set_refresh_cookie(response, refresh)
    return TokenOut(access_token=access)


@router.post("/refresh", response_model=TokenOut)
def refresh(request: Request):
    rt = request.cookies.get("refresh_token")
    if not rt:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh manquant")
    data = decode_token(rt)
    if data.get("typ") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="mauvais token")
    sub = data.get("sub")
    if not isinstance(sub, str):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="sub manquant")
    access = create_access_token(sub, data.get("org"))
    return TokenOut(access_token=access)


@router.post("/logout")
def logout(response: Response):
    clear_refresh_cookie(response)
    return {"status": "ok"}

@router.get("/me")
def me(current=Depends(get_current_account)):
    return {"id": current["id"], "email": current["email"], "org_id": current["org_id"]}


@router.post("/reset/request")
def reset_request(payload: ResetRequestIn, db: Session = Depends(get_db)):
    row = db.execute(text("SELECT id FROM accounts WHERE email=:e"), {"e": payload.email}).fetchone()
    if not row:
        # pour eviter user enumeration
        return {"status": "ok"}
    tok = create_reset_token(payload.email)
    # Pas d email a ce jalon; en dev on renvoie le token pour tests
    if settings.env == "dev":
        return {"status": "ok", "reset_token": tok}
    return {"status": "ok"}


@router.post("/reset/confirm")
def reset_confirm(payload: ResetConfirmIn, db: Session = Depends(get_db)):
    data = decode_token(payload.token)
    if data.get("typ") != "reset":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="token invalide")
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email manquant")
    new_hash = hash_password(payload.new_password)
    db.execute(text("UPDATE accounts SET password_hash=:ph WHERE email=:e"), {"ph": new_hash, "e": email})
    db.commit()
    return {"status": "ok"}
