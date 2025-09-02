from __future__ import annotations

import time

import jwt
import pytest

import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

from backend.app.services.tokens import sign_invite_token, verify_invite_token


def test_sign_and_verify():
    token, h = sign_invite_token("a1")
    assert isinstance(token, str)
    assert len(h) == 64
    data = verify_invite_token(token)
    assert data["sub"] == "a1"


def test_expired_token(monkeypatch):
    monkeypatch.setattr("backend.app.services.tokens.settings.INVITES_TTL_SECONDS", 1)
    token, _ = sign_invite_token("a2")
    time.sleep(2)
    with pytest.raises(jwt.ExpiredSignatureError):
        verify_invite_token(token)
