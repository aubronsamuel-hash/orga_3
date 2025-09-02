from backend.app.services.notifications.tokens import sign_token, verify_token, build_links


def test_sign_and_verify():
    tok = sign_token("secret", "assign-1", "user-1", ttl_sec=60)
    ok, info = verify_token("secret", tok)
    assert ok and info["assignment_id"] == "assign-1" and info["user_id"] == "user-1"
    links = build_links("http://x", tok)
    assert "accept" in links["accept_url"]
