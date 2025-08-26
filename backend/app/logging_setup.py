from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # noqa: D401
        data: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Extra champs si presents
        for k in ("request_id", "trace_id", "method", "path", "status", "duration_ms"):
            v = getattr(record, k, None)
            if v is not None:
                data[k] = v
        return json.dumps(data, separators=(",", ":"), ensure_ascii=True)


def configure_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    root = logging.getLogger()
    root.setLevel(level)
    # Nettoie handlers existants (evite doublons en tests)
    for h in list(root.handlers):
        root.removeHandler(h)
    h = logging.StreamHandler()
    h.setFormatter(JsonFormatter())
    root.addHandler(h)
