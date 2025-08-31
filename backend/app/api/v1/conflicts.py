from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException

from app.db import get_db
from app.services.conflicts import ConflictService
from app.schemas.conflicts import (
    ConflictItem,
    ConflictDetail,
    TimeWindow,
    ResolveRequest,
    ResolveResult,
    Suggestion,
)

router = APIRouter(prefix="/api/v1/conflicts", tags=["conflicts"])


def _svc(db) -> ConflictService:
    return ConflictService(db)


@router.get("", response_model=List[ConflictItem])
def list_conflicts(
    from_: datetime = Query(..., alias="from"),
    to: datetime = Query(..., alias="to"),
    db=Depends(get_db),
):
    svc = _svc(db)
    items = svc.find_conflicts(from_, to)
    return [
        ConflictItem(
            conflict_id=c.conflict_id,
            user_id=c.user_id,
            user_name=c.user_name,
            mission_ids=c.mission_ids,
            window=TimeWindow(start=c.start, end=c.end),
            reason=c.reason,
        )
        for c in items
    ]


@router.get("/{conflict_id}", response_model=ConflictDetail)
def get_conflict(
    conflict_id: str,
    from_: datetime = Query(..., alias="from"),
    to: datetime = Query(..., alias="to"),
    db=Depends(get_db),
):
    svc = _svc(db)
    conflicts = svc.find_conflicts(from_, to)
    c = next((x for x in conflicts if x.conflict_id == conflict_id), None)
    if not c:
        raise HTTPException(status_code=404, detail="Conflit introuvable")
    sugg = svc.suggest_replacements(c)
    return ConflictDetail(
        conflict=ConflictItem(
            conflict_id=c.conflict_id,
            user_id=c.user_id,
            user_name=c.user_name,
            mission_ids=c.mission_ids,
            window=TimeWindow(start=c.start, end=c.end),
            reason=c.reason,
        ),
        suggestions=[Suggestion(user_id=a.user_id, user_name=a.user_name) for a in sugg],
    )


@router.post("/resolve", response_model=ResolveResult)
def resolve(req: ResolveRequest, db=Depends(get_db)):
    svc = _svc(db)
    ok = svc.resolve(
        req.conflict_id, req.replace_assignment_mission_id, req.replacement_user_id
    )
    return ResolveResult(resolved=bool(ok), message="OK" if ok else "Echec")
