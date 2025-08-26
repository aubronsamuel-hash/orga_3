from __future__ import annotations
import json
import os
from typing import Any, Iterable, Optional, Tuple

DEFAULT_TTL = int(os.getenv("CACHE_TTL_SECONDS", "60"))
REDIS_URL = os.getenv("REDIS_URL", "fakeredis://")

redis: Any = None
fakeredis: Any = None
try:
    import redis as redis_lib
    redis = redis_lib
except Exception:  # pragma: no cover
    redis = None

try:
    import fakeredis as fakeredis_lib
    fakeredis = fakeredis_lib
except Exception:  # pragma: no cover
    fakeredis = None


class Cache:
    def __init__(self, client: Any):
        self.client = client

    def _k(self, key: str) -> str:
        return f"cc:{key}"

    def _tagk(self, tag: str) -> str:
        return f"cc:tag:{tag}"

    def get_json(self, key: str) -> Optional[Any]:
        raw = self.client.get(self._k(key))
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:  # pragma: no cover
            return None

    def set_json(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tags: Optional[Iterable[str]] = None,
    ) -> None:
        v = json.dumps(value, separators=(",", ":"), ensure_ascii=True)
        self.client.set(self._k(key), v, ex=ttl or DEFAULT_TTL)
        if tags:
            for t in tags:
                self.client.sadd(self._tagk(t), self._k(key))

    def invalidate_tags(self, tags: Iterable[str]) -> int:
        deleted = 0
        for t in tags:
            tag_key = self._tagk(t)
            members = list(self.client.smembers(tag_key) or [])
            if members:
                self.client.delete(*members)
                deleted += len(members)
            self.client.delete(tag_key)
        return deleted

    def cached_list(
        self,
        key: str,
        builder,
        ttl: Optional[int],
        tags: Iterable[str],
    ) -> Tuple[Any, bool]:
        v = self.get_json(key)
        if v is not None:
            return v, True
        data = builder()
        self.set_json(key, data, ttl=ttl, tags=tags)
        return data, False


_singleton: Optional[Cache] = None


def get_cache() -> Cache:
    global _singleton
    if _singleton:
        return _singleton
    url = REDIS_URL
    cli: Any
    if url.startswith("fakeredis://"):
        if not fakeredis:
            raise RuntimeError("fakeredis non disponible")
        cli = fakeredis.FakeRedis(decode_responses=True)
    else:
        if not redis:
            raise RuntimeError("redis non disponible")
        cli = redis.Redis.from_url(url, decode_responses=True)
    _singleton = Cache(cli)
    return _singleton
