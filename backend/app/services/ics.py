from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional

from sqlalchemy.orm import Session


class _Row(dict):
    pass


def default_loader(
    db: Session, project_id: str, date_from: datetime, date_to: datetime
) -> Iterable[_Row]:
    return []


def get_project_events(
    db: Session,
    *,
    project_id: str,
    date_from: datetime,
    date_to: datetime,
    loader: Optional[Callable[[Session, str, datetime, datetime], Iterable[_Row]]] = None,
) -> List[Dict[str, Any]]:
    if loader is None:
        loader = default_loader
    if date_from.tzinfo is None:
        date_from = date_from.replace(tzinfo=timezone.utc)
    if date_to.tzinfo is None:
        date_to = date_to.replace(tzinfo=timezone.utc)
    events: List[Dict[str, Any]] = []
    for r in loader(db, project_id, date_from, date_to):
        ev = {
            "uid": str(r.get("uid")),
            "dtstart": r.get("dtstart"),
            "dtend": r.get("dtend"),
            "summary": r.get("summary") or "Mission",
            "description": r.get("description") or "",
        }
        if not isinstance(ev["dtstart"], datetime) or not isinstance(ev["dtend"], datetime):
            continue
        if ev["dtstart"] >= ev["dtend"]:
            continue
        events.append(ev)
    return events

