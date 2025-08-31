from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TimeWindow(BaseModel):
    start: datetime
    end: datetime

class ConflictItem(BaseModel):
    conflict_id: str = Field(..., description="UUID logique concat mission_ids:user_id")
    user_id: int
    user_name: str
    mission_ids: List[int]
    window: TimeWindow
    reason: str = Field("DOUBLE_BOOKING")

class Suggestion(BaseModel):
    user_id: int
    user_name: str

class ConflictDetail(BaseModel):
    conflict: ConflictItem
    suggestions: List[Suggestion] = []

class ResolveRequest(BaseModel):
    conflict_id: str
    replace_assignment_mission_id: int
    replacement_user_id: int

class ResolveResult(BaseModel):
    resolved: bool
    message: str
