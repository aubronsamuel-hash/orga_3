"""core models jalon 3
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "0002_models_core"
down_revision = "0001_init_schema_meta"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orgs",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "accounts",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=36), sa.ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("org_id", "email", name="uq_accounts_org_email"),
    )
    op.create_index("ix_accounts_email", "accounts", ["email"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=36), sa.ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("account_id", sa.String(length=36), sa.ForeignKey("accounts.id", ondelete="SET NULL")),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column("employment_type", sa.String(length=20), nullable=False),
        sa.Column("rate_profile", sa.JSON(), nullable=True),
        sa.Column("legal_ids", sa.JSON(), nullable=True),
        sa.Column("documents", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("org_id", "account_id", name="uq_users_org_account"),
    )
    op.create_index("ix_users_last_name", "users", ["last_name"], unique=False)
    op.create_index("ix_users_first_name", "users", ["first_name"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=36), sa.ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default=sa.text("'DRAFT'")),
        sa.Column("starts_at", sa.DateTime(), nullable=True),
        sa.Column("ends_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("org_id", "name", name="uq_projects_org_name"),
        sa.CheckConstraint("(ends_at IS NULL) OR (starts_at IS NULL) OR (ends_at >= starts_at)", name="ck_project_dates"),
    )

    op.create_table(
        "missions",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=36), sa.ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("project_id", sa.String(length=36), sa.ForeignKey("projects.id", ondelete="SET NULL")),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("starts_at", sa.DateTime(), nullable=False),
        sa.Column("ends_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("ends_at >= starts_at", name="ck_mission_dates"),
    )
    op.create_index("ix_missions_starts_at", "missions", ["starts_at"], unique=False)
    op.create_index("ix_missions_ends_at", "missions", ["ends_at"], unique=False)
    op.create_index("ix_missions_project_id", "missions", ["project_id"], unique=False)

    op.create_table(
        "mission_roles",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("mission_id", sa.String(length=36), sa.ForeignKey("missions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role_name", sa.String(length=80), nullable=False),
        sa.Column("quota", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("mission_id", "role_name", name="uq_mission_role_name"),
    )

    op.create_table(
        "assignments",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("mission_id", sa.String(length=36), sa.ForeignKey("missions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default=sa.text("'INVITED'")),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_assignments_mission_user", "assignments", ["mission_id", "user_id"], unique=False)
    op.create_index(
        "uq_active_assignment_per_mission_user",
        "assignments",
        ["mission_id", "user_id"],
        unique=True,
        sqlite_where=sa.text("status IN ('INVITED','ACCEPTED')"),
        postgresql_where=sa.text("status IN ('INVITED','ACCEPTED')"),
    )

    op.create_table(
        "availability",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=36), sa.ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("starts_at", sa.DateTime(), nullable=False),
        sa.Column("ends_at", sa.DateTime(), nullable=False),
        sa.Column("note", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("ends_at >= starts_at", name="ck_availability_dates"),
    )
    op.create_index("ix_availability_starts_at", "availability", ["starts_at"], unique=False)
    op.create_index("ix_availability_ends_at", "availability", ["ends_at"], unique=False)

    op.create_table(
        "invitations",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=36), sa.ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mission_id", sa.String(length=36), sa.ForeignKey("missions.id", ondelete="SET NULL")),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("token", sa.String(length=64), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("revoked", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "user_skills",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("skill", sa.String(length=80), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "skill", name="uq_user_skill"),
    )

    op.create_table(
        "user_tags",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tag", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "tag", name="uq_user_tag"),
    )

    op.create_table(
        "audit_log",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=36), sa.ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("actor_account_id", sa.String(length=36), sa.ForeignKey("accounts.id", ondelete="SET NULL")),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_log")
    op.drop_table("user_tags")
    op.drop_table("user_skills")
    op.drop_table("invitations")
    op.drop_index("ix_availability_ends_at", table_name="availability")
    op.drop_index("ix_availability_starts_at", table_name="availability")
    op.drop_table("availability")
    op.drop_index("uq_active_assignment_per_mission_user", table_name="assignments")
    op.drop_index("ix_assignments_mission_user", table_name="assignments")
    op.drop_table("assignments")
    op.drop_table("mission_roles")
    op.drop_index("ix_missions_project_id", table_name="missions")
    op.drop_index("ix_missions_ends_at", table_name="missions")
    op.drop_index("ix_missions_starts_at", table_name="missions")
    op.drop_table("missions")
    op.drop_table("projects")
    op.drop_index("ix_users_first_name", table_name="users")
    op.drop_index("ix_users_last_name", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_accounts_email", table_name="accounts")
    op.drop_table("accounts")
    op.drop_table("orgs")
