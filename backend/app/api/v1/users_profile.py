from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models.availability import (
    Availability,
    AvailabilityStatus,
    EmploymentType as ModelEmploymentType,
    UserProfile,
)
from backend.app.schemas.availability import (
    EmploymentType as SchemaEmploymentType,
    UserProfileIn,
    UserProfileOut,
)

router = APIRouter()


@router.get("/{user_id}/profile", response_model=UserProfileOut)
def get_profile(user_id: str = Path(...), db: Session = Depends(get_db)):
    prof = db.query(UserProfile).filter(UserProfile.user_id == user_id).one_or_none()
    if not prof:
        raise HTTPException(status_code=404, detail="profil introuvable")
    return UserProfileOut(
        user_id=prof.user_id,
        skills=prof.skills,
        tags=prof.tags,
        employment_type=SchemaEmploymentType(prof.employment_type),
        rate_profile=prof.rate_profile,
        bio=prof.bio,
    )


@router.put("/{user_id}/profile", response_model=UserProfileOut)
def upsert_profile(
    user_id: str, payload: UserProfileIn, db: Session = Depends(get_db)
):
    prof = db.query(UserProfile).filter(UserProfile.user_id == user_id).one_or_none()
    if not prof:
        prof = UserProfile(user_id=user_id)
    prof.skills = payload.skills
    prof.tags = payload.tags
    prof.employment_type = ModelEmploymentType(payload.employment_type)
    prof.rate_profile = payload.rate_profile
    prof.bio = payload.bio
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return UserProfileOut(
        user_id=prof.user_id,
        skills=prof.skills,
        tags=prof.tags,
        employment_type=SchemaEmploymentType(prof.employment_type),
        rate_profile=prof.rate_profile,
        bio=prof.bio,
    )


@router.get("/{user_id}/calendar", response_model=List[dict])
def user_calendar(
    user_id: str,
    from_: datetime = Query(..., alias="from"),
    to: datetime = Query(..., alias="to"),
    db: Session = Depends(get_db),
):
    items = (
        db.query(Availability)
        .filter(
            Availability.user_id == user_id,
            Availability.status == AvailabilityStatus.APPROVED,
            Availability.start_at >= from_.replace(tzinfo=None),
            Availability.end_at <= to.replace(tzinfo=None),
        )
        .order_by(Availability.start_at.asc())
        .all()
    )
    return [
        {
            "id": x.id,
            "start_at": x.start_at,
            "end_at": x.end_at,
            "status": x.status,
        }
        for x in items
    ]
