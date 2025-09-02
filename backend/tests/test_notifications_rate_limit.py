from app.services.notifications.rate_limit import RateLimiter


def test_rate_limit_mem_window():
    rl = RateLimiter()
    hits = 0
    for _ in range(6):
        hits = rl.hit("k", 1)
    assert hits == 6
