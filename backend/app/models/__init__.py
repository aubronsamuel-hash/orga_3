from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.enums import AssignmentStatus, ProjectStatus


def _uuid() -> str:
    return str(uuid.uuid4())


class TSMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow(), nullable=False
    )


class Org(Base, TSMixin):
    __tablename__ = "orgs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)


class Account(Base, TSMixin):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("org_id", "email", name="uq_accounts_org_email"),
        Index("ix_accounts_email", "email"),
    )


class User(Base, TSMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="SET NULL"))
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    employment_type: Mapped[str] = mapped_column(String(20), nullable=False)
    rate_profile: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    legal_ids: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    documents: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        Index("ix_users_last_name", "last_name"),
        Index("ix_users_first_name", "first_name"),
        UniqueConstraint("org_id", "account_id", name="uq_users_org_account", deferrable=False, initially=None),
    )


class UserSkill(Base, TSMixin):
    __tablename__ = "user_skills"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill: Mapped[str] = mapped_column(String(80), nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "skill", name="uq_user_skill"),)


class UserTag(Base, TSMixin):
    __tablename__ = "user_tags"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tag: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "tag", name="uq_user_tag"),)


class Project(Base, TSMixin):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(16), default=ProjectStatus.DRAFT.value, nullable=False)
    starts_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("org_id", "name", name="uq_projects_org_name"),
        CheckConstraint(
            "(ends_at IS NULL) OR (starts_at IS NULL) OR (ends_at >= starts_at)",
            name="ck_project_dates",
        ),
    )


class Mission(Base, TSMixin):
    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("projects.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        CheckConstraint("ends_at >= starts_at", name="ck_mission_dates"),
        Index("ix_missions_starts_at", "starts_at"),
        Index("ix_missions_ends_at", "ends_at"),
        Index("ix_missions_project_id", "project_id"),
    )


class MissionRole(Base, TSMixin):
    __tablename__ = "mission_roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    mission_id: Mapped[str] = mapped_column(String(36), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    role_name: Mapped[str] = mapped_column(String(80), nullable=False)
    quota: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __table_args__ = (UniqueConstraint("mission_id", "role_name", name="uq_mission_role_name"),)


class Assignment(Base, TSMixin):
    __tablename__ = "assignments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    mission_id: Mapped[str] = mapped_column(String(36), ForeignKey("missions.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(String(16), default=AssignmentStatus.INVITED.value, nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_assignments_mission_user", "mission_id", "user_id"),
    )


class Availability(Base, TSMixin):
    __tablename__ = "availability"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    note: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    __table_args__ = (
        CheckConstraint("ends_at >= starts_at", name="ck_availability_dates"),
        Index("ix_availability_starts_at", "starts_at"),
        Index("ix_availability_ends_at", "ends_at"),
    )


class Invitation(Base):
    __tablename__ = "invitations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    assignment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow(), nullable=False)

    __table_args__ = (
        Index("ix_invitations_token_hash", "token_hash"),
        Index("ix_invitations_expires_at", "expires_at"),
    )


class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    org_id: Mapped[str] = mapped_column(String(36), ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False)
    actor_account_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("accounts.id", ondelete="SET NULL"))
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
