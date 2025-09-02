from __future__ import annotations

from typing import Optional, Protocol


class _RedisLike(Protocol):
    def incr(self, key: str) -> int: ...

    def expire(self, key: str, seconds: int) -> None: ...


class InMemoryBucket:
    def __init__(self) -> None:
        self._store: dict[str, list[float]] = {}

    def hit(self, key: str, window_sec: int) -> int:
        import time

        now = time.time()
        arr = [t for t in self._store.get(key, []) if now - t < window_sec]
        arr.append(now)
        self._store[key] = arr
        return len(arr)


class RateLimiter:
    def __init__(self, redis_client: Optional[_RedisLike] = None) -> None:
        self.redis: Optional[_RedisLike] = redis_client
        self.mem: Optional[InMemoryBucket] = None if redis_client else InMemoryBucket()

    def hit(self, key: str, window_sec: int) -> int:
        if self.redis is not None:
            c = self.redis.incr(key)
            if c == 1:
                self.redis.expire(key, window_sec)
            return int(c)
        assert self.mem is not None
        return self.mem.hit(key, window_sec)

