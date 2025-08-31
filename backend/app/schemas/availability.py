from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class EmploymentType(str, Enum):
    CDI = "CDI"
    CDD = "CDD"
    FREELANCE = "FREELANCE"
    INTERMITTENT = "INTERMITTENT"
    OTHER = "OTHER"


class AvailabilityStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class UserProfileIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skills: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    employment_type: EmploymentType = EmploymentType.INTERMITTENT
    rate_profile: Dict[str, float] = Field(default_factory=dict)
    bio: Optional[str] = None


class UserProfileOut(UserProfileIn):
    user_id: str


class AvailabilityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str
    start_at: datetime
    end_at: datetime
    note: Optional[str] = None


class AvailabilityOut(BaseModel):
    id: str
    user_id: str
    start_at: datetime
    end_at: datetime
    status: AvailabilityStatus
    note: Optional[str] = None
