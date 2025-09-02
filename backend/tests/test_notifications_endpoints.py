from fastapi.testclient import TestClient
from app.main import create_app
from app.routers import notifications as notif_router

app = create_app()


def test_test_email_endpoint(monkeypatch):
    def fake_send(*args, **kwargs):
        return {"ok": True}

    monkeypatch.setattr(notif_router, "send_email", fake_send)
    c = TestClient(app)
    r = c.post(
        "/api/v1/notifications/test-email",
        json={
            "to": "dev@example.test",
            "subject": "Ping",
            "template": "invite",
            "context": {
                "user_name": "S",
                "mission": "M",
                "accept_url": "a",
                "decline_url": "d",
            },
        },
    )
    assert r.status_code == 202


def test_send_invitation_dry_run(monkeypatch):
    c = TestClient(app)
    r = c.post(
        "/api/v1/invitations/send",
        json={
            "user_id": "u1",
            "user_email": "dev@example.test",
            "assignment_id": "a1",
            "mission_name": "M1",
            "channels": ["email"],
            "dry_run": True,
        },
    )
    assert r.status_code == 202
    data = r.json()
    assert data["results"]["email"] == "queued"
    assert "accept_url" in data["links"]
