from __future__ import annotations

from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class MonthlyUserItem(BaseModel):
    user_id: str = Field(..., description="UUID user en string")
    user_name: str
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$", description="AAAA-MM en UTC")
    hours_planned: float = Field(ge=0)
    hours_confirmed: float = Field(ge=0)
    amount: float = Field(ge=0)


class MonthlyUsersResponse(BaseModel):
    org_id: str
    project_id: Optional[str] = None
    date_from: date
    date_to: date
    items: List[MonthlyUserItem]
    currency: Literal["EUR"] = "EUR"
