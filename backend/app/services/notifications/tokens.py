import base64
import hashlib
import hmac
import time


def sign_token(secret: str, assignment_id: str, user_id: str, ttl_sec: int = 7 * 24 * 3600) -> str:
    exp = int(time.time()) + ttl_sec
    payload = f"{assignment_id}|{user_id}|{exp}"
    sig = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(payload.encode("utf-8") + b"." + sig).decode("ascii")
    return token


def verify_token(secret: str, token: str) -> tuple[bool, dict | None]:
    try:
        raw = base64.urlsafe_b64decode(token.encode("ascii"))
        payload_raw, sig = raw.split(b".", 1)
        expected = hmac.new(secret.encode("utf-8"), payload_raw, hashlib.sha256).digest()
        if not hmac.compare_digest(sig, expected):
            return False, None
        payload = payload_raw.decode("utf-8")
        assignment_id, user_id, exp_s = payload.split("|")
        if int(exp_s) < int(time.time()):
            return False, None
        return True, {"assignment_id": assignment_id, "user_id": user_id}
    except Exception:
        return False, None


def build_links(base_url: str, token: str) -> dict:
    return {
        "accept_url": f"{base_url}/accept?t={token}",
        "decline_url": f"{base_url}/decline?t={token}",
    }
