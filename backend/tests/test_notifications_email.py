import types

from app.services.notifications import email as email_svc


class DummySMTP:
    def __init__(self, host, port, timeout=10):
        self.sent = False

    def __enter__(self):  # noqa: D401
        return self

    def __exit__(self, exc_type, exc, tb):  # noqa: D401
        return False

    def starttls(self):  # noqa: D401
        return None

    def login(self, u, p):  # noqa: D401
        return None

    def send_message(self, msg):  # noqa: D401
        self.sent = True


def test_send_email_monkeypatch(monkeypatch):
    monkeypatch.setattr(email_svc, "smtplib", types.SimpleNamespace(SMTP=DummySMTP))
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
