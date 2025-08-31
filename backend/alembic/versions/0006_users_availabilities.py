"""Jalon 16 users profiles and availabilities"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "0006_users_availabilities"
down_revision = "0005_invitations_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    tables = inspect(bind).get_table_names()

    if "user_profiles" not in tables:
        op.create_table(
            "user_profiles",
            sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
            sa.Column(
                "user_id",
                sa.String(length=36),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                nullable=False,
                unique=True,
            ),
            sa.Column("skills", sa.JSON(), nullable=False, server_default="[]"),
            sa.Column("tags", sa.JSON(), nullable=False, server_default="[]"),
            sa.Column(
                "employment_type",
                sa.Enum(
                    "CDI",
                    "CDD",
                    "FREELANCE",
                    "INTERMITTENT",
                    "OTHER",
                    name="employment_type",
                ),
                nullable=False,
                server_default="INTERMITTENT",
            ),
            sa.Column("rate_profile", sa.JSON(), nullable=False, server_default="{}"),
            sa.Column("bio", sa.Text(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
        )

    if "availabilities" not in tables:
        op.create_table(
            "availabilities",
            sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
            sa.Column(
                "user_id",
                sa.String(length=36),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("start_at", sa.DateTime(), nullable=False),
            sa.Column("end_at", sa.DateTime(), nullable=False),
            sa.Column(
                "status",
                sa.Enum("PENDING", "APPROVED", "REJECTED", name="availability_status"),
                nullable=False,
                server_default="PENDING",
            ),
            sa.Column("note", sa.String(length=255), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
            sa.UniqueConstraint(
                "user_id", "start_at", "end_at", name="uq_availability_exact_slot"
            ),
        )
        op.create_index(
            "ix_availability_user_status",
            "availabilities",
            ["user_id", "status"],
        )

    if "availability_actions" not in tables:
        op.create_table(
            "availability_actions",
            sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
            sa.Column(
                "availability_id",
                sa.String(length=36),
                sa.ForeignKey("availabilities.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("action", sa.String(length=32), nullable=False),
            sa.Column("actor_id", sa.String(length=36), nullable=True),
            sa.Column(
                "at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
            sa.Column("meta", sa.JSON(), nullable=False, server_default="{}"),
        )


def downgrade() -> None:
    bind = op.get_bind()
    tables = inspect(bind).get_table_names()

    if "availability_actions" in tables:
        op.drop_table("availability_actions")
    if "availabilities" in tables:
        op.drop_index("ix_availability_user_status", table_name="availabilities")
        op.drop_constraint(
            "uq_availability_exact_slot", "availabilities", type_="unique"
        )
        op.drop_table("availabilities")
    if "user_profiles" in tables:
        op.drop_table("user_profiles")
    op.execute("DROP TYPE IF EXISTS employment_type")
    op.execute("DROP TYPE IF EXISTS availability_status")
