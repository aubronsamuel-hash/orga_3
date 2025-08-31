from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.availability import Availability, AvailabilityStatus as ModelStatus
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityOut,
    AvailabilityStatus,
)
from app.services.availability_service import (
    BadRequest,
    NotFound,
    request_availability,
    set_status,
)

router = APIRouter()


@router.post("", response_model=AvailabilityOut, status_code=200)
def create_availability(payload: AvailabilityCreate, db: Session = Depends(get_db)):
    try:
        av = request_availability(
            db, payload.user_id, payload.start_at, payload.end_at, payload.note
        )
        return AvailabilityOut(**av.__dict__)
    except BadRequest as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{availability_id}:approve", response_model=AvailabilityOut)
def approve_availability(
    availability_id: str = Path(...), db: Session = Depends(get_db)
):
    try:
        av = set_status(db, availability_id, ModelStatus.APPROVED)
        return AvailabilityOut(**av.__dict__)
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequest as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/{availability_id}:reject", response_model=AvailabilityOut)
def reject_availability(
    availability_id: str = Path(...), db: Session = Depends(get_db)
):
    try:
        av = set_status(db, availability_id, ModelStatus.REJECTED)
        return AvailabilityOut(**av.__dict__)
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("", response_model=List[AvailabilityOut])
def list_availabilities(
    user_id: Optional[str] = Query(default=None),
    status: Optional[AvailabilityStatus] = Query(default=None),
    from_: Optional[datetime] = Query(default=None, alias="from"),
    to: Optional[datetime] = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
):
    stmt = select(Availability)
    if user_id is not None:
        stmt = stmt.where(Availability.user_id == user_id)
    if status is not None:
        stmt = stmt.where(Availability.status == ModelStatus(status))
    if from_ is not None:
        stmt = stmt.where(Availability.start_at >= from_.replace(tzinfo=None))
    if to is not None:
        stmt = stmt.where(Availability.end_at <= to.replace(tzinfo=None))
    stmt = stmt.order_by(Availability.start_at.asc())
    rows = db.execute(stmt).scalars().all()
    return [AvailabilityOut(**r.__dict__) for r in rows]
