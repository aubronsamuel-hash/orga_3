from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..config import settings
from ..services.notifications.email import send_email
from ..services.notifications.telegram import send_telegram
from ..services.notifications.compose import render_template
from ..services.notifications.tokens import (
    sign_token,
    build_links,
    verify_token,
)
from ..services.notifications.rate_limit import RateLimiter


router = APIRouter(prefix="/api/v1", tags=["notifications"])

# simple in-memory limiter by default
limiter = RateLimiter()


class TestEmailPayload(BaseModel):
    to: str
    subject: str
    template: str
    context: dict


@router.post("/notifications/test-email", status_code=202)
def notifications_test_email(p: TestEmailPayload):
    try:
        send_email(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            settings.SMTP_USER,
            settings.SMTP_PASSWORD,
            settings.SMTP_FROM,
            p.to,
            p.subject,
            p.template,
            p.context,
        )
        return {"status": "sent"}
    except Exception as e:  # pragma: no cover - simple proxy
        raise HTTPException(status_code=502, detail=f"Erreur envoi SMTP: {e}")


class InviteRequest(BaseModel):
    user_id: str
    user_email: str | None = None
    telegram_chat_id: str | None = None
    assignment_id: str
    mission_name: str
    channels: list[str] = ["email"]
    dry_run: bool = False


@router.post("/invitations/send", status_code=202)
def send_invitation(req: InviteRequest):
    key = f"invite:{req.user_id}"
    hits = limiter.hit(key, settings.INVITE_RATE_LIMIT_WINDOW_SEC)
    if hits > settings.INVITE_RATE_LIMIT_COUNT:
        raise HTTPException(
            status_code=429, detail="Trop de tentatives d envoi. Reessayer plus tard."
        )
    token = sign_token(settings.SIGNING_SECRET, req.assignment_id, req.user_id)
    links = build_links(settings.INVITE_LINK_BASE_URL, token)
    context = {
        "user_name": req.user_id,
        "mission": req.mission_name,
        "accept_url": links["accept_url"],
        "decline_url": links["decline_url"],
    }
    results = {}
    if "email" in req.channels:
        if not req.user_email:
            raise HTTPException(status_code=400, detail="Email cible manquant.")
        if not req.dry_run:
            send_email(
                settings.SMTP_HOST,
                settings.SMTP_PORT,
                settings.SMTP_USER,
                settings.SMTP_PASSWORD,
                settings.SMTP_FROM,
                req.user_email,
                f"Invitation: {req.mission_name}",
                "invite",
                context,
            )
        results["email"] = "queued" if req.dry_run else "sent"
    if "telegram" in req.channels:
        if not (
            settings.TELEGRAM_BOT_TOKEN
            and (req.telegram_chat_id or settings.TELEGRAM_DEFAULT_CHAT_ID)
        ):
            raise HTTPException(status_code=400, detail="Telegram non configure.")
        if not req.dry_run:
            send_telegram(
                settings.TELEGRAM_BOT_TOKEN,
                req.telegram_chat_id or settings.TELEGRAM_DEFAULT_CHAT_ID,
                render_template("invite", context),
            )
        results["telegram"] = "queued" if req.dry_run else "sent"
    return {"ok": True, "results": results, "links": links}


class VerifyTokenResp(BaseModel):
    ok: bool
    assignment_id: str | None = None
    user_id: str | None = None


@router.get("/invitations/verify", response_model=VerifyTokenResp)
def verify_invitation_token(t: str = Query(..., description="token signe")):
    ok, info = verify_token(settings.SIGNING_SECRET, t)
    if not ok:
        return VerifyTokenResp(ok=False)
    return VerifyTokenResp(ok=True, assignment_id=info["assignment_id"], user_id=info["user_id"])


@router.get("/notifications")
def list_notifications(status: str | None = None):
    return {"items": [], "status_filter": status or "all"}
