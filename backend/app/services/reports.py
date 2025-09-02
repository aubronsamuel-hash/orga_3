from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Tuple

from sqlalchemy.orm import Session
from ..core.cache import get_reports_cache
import os


@dataclass(frozen=True)
class _Row:
    user_id: str
    user_name: str
    start_utc: datetime
    end_utc: datetime
    status: str
    rate_type: Optional[str]
    rate_amount: Optional[float]
    confirmed_hours: Optional[float]


def _month_key(dt: datetime) -> str:
    dt = dt.astimezone(timezone.utc)
    return f"{dt.year:04d}-{dt.month:02d}"


def _hours_between(a: datetime, b: datetime) -> float:
    return max((b - a).total_seconds(), 0.0) / 3600.0


def compute_monthly_totals(
    db: Session,
    *,
    org_id: str,
    project_id: Optional[str],
    date_from: datetime,
    date_to: datetime,
) -> List[Dict]:
    # NOTE: Implementation kept simple; adapt joins to your schema.
    # Expected tables: users, missions, mission_assignments, projects
    # Only ACCEPTED contribute to confirmed hours and amounts.
    # Planned hours = mission duration regardless of assignment status.
    # Replace this with optimized SQL if needed.
    # Pseudo-query replaced by placeholder loader to keep tests agnostic.
    rows: Iterable[_Row] = []  # Replace by real query in integration.
    agg: Dict[Tuple[str, str, str], Dict] = {}
    for r in rows:
        m = _month_key(r.start_utc)
        key = (r.user_id, r.user_name, m)
        if key not in agg:
            agg[key] = {
                "user_id": r.user_id,
                "user_name": r.user_name,
                "month": m,
                "hours_planned": 0.0,
                "hours_confirmed": 0.0,
                "amount": 0.0,
            }
        planned = _hours_between(r.start_utc, r.end_utc)
        agg[key]["hours_planned"] += planned
        if r.status == "ACCEPTED":
            confirmed = r.confirmed_hours if r.confirmed_hours is not None else planned
            agg[key]["hours_confirmed"] += confirmed
            if r.rate_type == "hourly" and r.rate_amount:
                agg[key]["amount"] += confirmed * r.rate_amount
            elif r.rate_type == "flat" and r.rate_amount:
                agg[key]["amount"] += r.rate_amount
    items = list(agg.values())
    items.sort(key=lambda x: (x["user_name"], x["month"]))
    return items


def compute_monthly_totals_cached(
    db: Session,
    *,
    org_id: str,
    project_id: Optional[str],
    date_from: datetime,
    date_to: datetime,
) -> List[Dict]:
    ttl = int(os.environ.get("REPORTS_CACHE_TTL_SECONDS", "300"))
    cache = get_reports_cache(ttl)
    key = (org_id, project_id or "", date_from.isoformat(), date_to.isoformat())

    def _factory() -> List[Dict]:
        return compute_monthly_totals(
            db,
            org_id=org_id,
            project_id=project_id,
            date_from=date_from,
            date_to=date_to,
        )

    return cache.get_or_set(key, _factory)
