from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

ConflictKind = Literal["ASSIGNMENT_OVERLAP"]


class ConflictItem(BaseModel):
    kind: ConflictKind = Field(default="ASSIGNMENT_OVERLAP")
    user_id: str
    mission_id: str
    starts_at: str
    ends_at: str
    with_mission_id: Optional[str] = None


class ConflictList(BaseModel):
    user_id: str
    items: List[ConflictItem] = Field(default_factory=list)

