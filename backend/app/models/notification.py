from __future__ import annotations

import enum
import uuid
from sqlalchemy import Column, String, DateTime, Enum, JSON, func
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Channel(str, enum.Enum):
    email = "email"
    telegram = "telegram"


class NotificationType(str, enum.Enum):
    invite = "invite"
    reminder = "reminder"
    schedule_change = "schedule_change"
    cancellation = "cancellation"


class NotificationStatus(str, enum.Enum):
    queued = "queued"
    sent = "sent"
    failed = "failed"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    channel = Column(Enum(Channel), nullable=False)
    ntype = Column(Enum(NotificationType), nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(
        Enum(NotificationStatus), nullable=False, default=NotificationStatus.queued
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    read_at = Column(DateTime(timezone=True), nullable=True)
