from __future__ import annotations

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.conflicts import ConflictList
from app.services import conflicts as conflicts_service


router = APIRouter(prefix="/api/v1/conflicts", tags=["conflicts"])


@router.get("/user/{user_id}", response_model=ConflictList)
def get_user_conflicts(
    user_id: str = Path(..., min_length=1),
    db: Session = Depends(get_db),
) -> ConflictList:
    return conflicts_service.list_user_conflicts(db, user_id=user_id)

