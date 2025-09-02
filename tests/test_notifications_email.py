
# Aligner les imports sur le package existant: app.*

from app.services.notifications import email as email_svc

import types


class DummySMTP:
    def __init__(self, host, port, timeout=10):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def starttls(self):
        pass

    def login(self, u, p):
        pass

    def send_message(self, msg):
        self.sent = True


def test_send_email_monkeypatch(monkeypatch):
    monkeypatch.setattr(
        email_svc, "smtplib", types.SimpleNamespace(SMTP=DummySMTP)
    )
    res = email_svc.send_email(
        "localhost",
        1025,
        None,
        None,
        "no-reply@test",
        "dev@test",
        "Subj",
        "invite",
        {
            "user_name": "Sam",
            "mission": "Covertramp",
            "accept_url": "a",
            "decline_url": "d",
        },
    )
    assert res["ok"] is True

