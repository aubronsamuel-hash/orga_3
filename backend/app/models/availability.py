from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models import TSMixin, _uuid


class EmploymentType(str, enum.Enum):
    CDI = "CDI"
    CDD = "CDD"
    FREELANCE = "FREELANCE"
    INTERMITTENT = "INTERMITTENT"
    OTHER = "OTHER"


class AvailabilityStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class UserProfile(Base, TSMixin):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True)
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    employment_type: Mapped[EmploymentType] = mapped_column(Enum(EmploymentType), default=EmploymentType.INTERMITTENT)
    rate_profile: Mapped[dict] = mapped_column(JSON, default=dict)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class Availability(Base, TSMixin):
    __tablename__ = "availabilities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    start_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[AvailabilityStatus] = mapped_column(
        Enum(AvailabilityStatus), default=AvailabilityStatus.PENDING, index=True
    )
    note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "start_at", "end_at", name="uq_availability_exact_slot"),
    )


class AvailabilityAction(Base):
    __tablename__ = "availability_actions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    availability_id: Mapped[str] = mapped_column(String(36), ForeignKey("availabilities.id", ondelete="CASCADE"), index=True)
    action: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="SET NULL"), nullable=True)
    at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    meta: Mapped[dict] = mapped_column(JSON, default=dict)
