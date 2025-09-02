from __future__ import annotations

import time
from threading import RLock
from typing import Any, Callable, Dict, Hashable, Optional, Tuple


class TTLCache:
    def __init__(self, ttl_seconds: int = 300, max_items: int = 1024) -> None:
        self.ttl = ttl_seconds
        self.max = max_items
        self._data: Dict[Hashable, Tuple[float, Any]] = {}
        self._lock = RLock()

    def get_or_set(self, key: Hashable, factory: Callable[[], Any]) -> Any:
        now = time.time()
        with self._lock:
            hit = self._data.get(key)
            if hit:
                exp, val = hit
                if exp > now:
                    return val
                self._data.pop(key, None)
            val = factory()
            if len(self._data) >= self.max:
                oldest_key = min(self._data, key=lambda k: self._data[k][0], default=None)
                if oldest_key is not None:
                    self._data.pop(oldest_key, None)
            self._data[key] = (now + self.ttl, val)
            return val


_reports_cache: Optional[TTLCache] = None


def get_reports_cache(ttl_seconds: int) -> TTLCache:
    global _reports_cache
    if _reports_cache is None or _reports_cache.ttl != ttl_seconds:
        _reports_cache = TTLCache(ttl_seconds=ttl_seconds)
    return _reports_cache

