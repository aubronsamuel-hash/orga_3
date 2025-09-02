from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...schemas.reports import MonthlyUserItem, MonthlyUsersResponse
from ...services.reports import compute_monthly_totals_cached
from ...db import get_db

# Alias pour compatibilité des tests: le nom historique
# ``compute_monthly_totals`` est toujours monkeypatché.
compute_monthly_totals = compute_monthly_totals_cached

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/monthly-users", response_model=MonthlyUsersResponse)
def monthly_users(
    org_id: str = Query(..., description="UUID organisation"),
    project_id: Optional[str] = Query(None, description="UUID projet"),
    date_from: str = Query(..., description="YYYY-MM-DD UTC"),
    date_to: str = Query(..., description="YYYY-MM-DD UTC"),
    db: Session = Depends(get_db),
):
    try:
        df = datetime.fromisoformat(date_from).replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(date_to).replace(tzinfo=timezone.utc)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Dates invalides: format attendu YYYY-MM-DD.",
        )
    if df > dt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plage de dates invalide: date_from > date_to.",
        )
    # Utilise l'alias compatible pour permettre le monkeypatch dans les tests.
    items = compute_monthly_totals(
        db, org_id=org_id, project_id=project_id, date_from=df, date_to=dt
    )
    return MonthlyUsersResponse(
        org_id=org_id,
        project_id=project_id,
        date_from=df.date(),
        date_to=dt.date(),
        items=[MonthlyUserItem(**it) for it in items],
    )
