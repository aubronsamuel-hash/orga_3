from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from backend.app.models.availability import Availability, AvailabilityStatus


class BadRequest(Exception):
    pass


class NotFound(Exception):
    pass


def _ensure_slot_valid(start_at: datetime, end_at: datetime) -> None:
    if end_at <= start_at:
        raise BadRequest("end must be after start")


def _has_overlap(db: Session, user_id: str, start_at: datetime, end_at: datetime) -> bool:
    q = select(Availability).where(
        Availability.user_id == user_id,
        Availability.status == AvailabilityStatus.APPROVED,
        or_(
            and_(Availability.start_at <= start_at, Availability.end_at > start_at),
            and_(Availability.start_at < end_at, Availability.end_at >= end_at),
            and_(Availability.start_at >= start_at, Availability.end_at <= end_at),
        ),
    )
    return db.execute(q).first() is not None


def request_availability(
    db: Session,
    user_id: str,
    start_at: datetime,
    end_at: datetime,
    note: Optional[str],
) -> Availability:
    start = start_at.replace(tzinfo=None)
    end = end_at.replace(tzinfo=None)
    _ensure_slot_valid(start, end)
    av = Availability(user_id=user_id, start_at=start, end_at=end, note=note)
    db.add(av)
    db.commit()
    db.refresh(av)
    return av


def set_status(db: Session, availability_id: str, status: AvailabilityStatus) -> Availability:
    av = db.get(Availability, availability_id)
    if not av:
        raise NotFound("availability not found")
    if status == AvailabilityStatus.APPROVED:
        if _has_overlap(db, av.user_id, av.start_at, av.end_at):
            raise BadRequest("overlap with existing approved slot")
    av.status = status
    db.add(av)
    db.commit()
    db.refresh(av)
    return av
