from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from ...services.reports import compute_monthly_totals
from ...services.exports import to_csv_monthly_users, to_pdf_monthly_users, to_ics
from ...db import get_db

router = APIRouter(prefix="/api/v1/exports", tags=["exports"])


@router.get("/csv")
def export_csv(
    type: str = Query(..., description="monthly-users"),
    org_id: str = Query(...),
    project_id: Optional[str] = Query(None),
    date_from: str = Query(...),
    date_to: str = Query(...),
    db: Session = Depends(get_db),
):
    if type != "monthly-users":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type d export non supporte.",
        )
    try:
        df = datetime.fromisoformat(date_from).replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(date_to).replace(tzinfo=timezone.utc)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Dates invalides.")
    items = compute_monthly_totals(
        db, org_id=org_id, project_id=project_id, date_from=df, date_to=dt
    )
    data = to_csv_monthly_users(items)
    filename = f"monthly-users_{org_id}*{df.date()}*{dt.date()}.csv"
    return Response(
        content=data,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/pdf")
def export_pdf(
    type: str = Query(..., description="monthly-users"),
    org_id: str = Query(...),
    project_id: Optional[str] = Query(None),
    date_from: str = Query(...),
    date_to: str = Query(...),
    db: Session = Depends(get_db),
):
    if type != "monthly-users":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type d export non supporte.",
        )
    try:
        df = datetime.fromisoformat(date_from).replace(tzinfo=timezone.utc)
        dt = datetime.fromisoformat(date_to).replace(tzinfo=timezone.utc)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Dates invalides.")
    items = compute_monthly_totals(
        db, org_id=org_id, project_id=project_id, date_from=df, date_to=dt
    )
    try:
        pdf = to_pdf_monthly_users(items)
    except RuntimeError as e:
        if str(e) == "PDF_EXPORT_UNAVAILABLE":
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Export PDF indisponible (dependance manquante).",
            )
        raise
    filename = f"monthly-users_{org_id}*{df.date()}*{dt.date()}.pdf"
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/ics")
def export_ics(
    project_id: str = Query(...),
    date_from: str = Query(...),
    date_to: str = Query(...),
    db: Session = Depends(get_db),
):
    # Placeholder: real implementation should query assignments
    events: list[dict] = []
    ics = to_ics(events)
    filename = f"project-{project_id}*{date_from}*{date_to}.ics"
    return Response(
        content=ics,
        media_type="text/calendar; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
