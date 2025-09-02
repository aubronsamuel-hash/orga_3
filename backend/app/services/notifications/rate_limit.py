import time
from typing import Optional


class InMemoryBucket:
    def __init__(self) -> None:
        self._store: dict[str, list[float]] = {}

    def hit(self, key: str, window_sec: int) -> int:
        now = time.time()
        arr = [t for t in self._store.get(key, []) if now - t < window_sec]
        arr.append(now)
        self._store[key] = arr
        return len(arr)


class RateLimiter:
    def __init__(self, redis_client: Optional[object] = None) -> None:
        self.redis = redis_client
        self.mem = InMemoryBucket() if redis_client is None else None

    def hit(self, key: str, window_sec: int) -> int:
        if self.redis:
            c = self.redis.incr(key)
            if c == 1:
                self.redis.expire(key, window_sec)
            return int(c)
        return self.mem.hit(key, window_sec)
