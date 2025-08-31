"""Jalon 15.5 invitations table"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0005_invitations_table"
down_revision = "0004_rbac_org_memberships"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "invitations",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("assignment_id", sa.String(length=36), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["assignment_id"], ["assignments.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_invitations_token_hash", "invitations", ["token_hash"], unique=False)
    op.create_index("ix_invitations_expires_at", "invitations", ["expires_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_invitations_token_hash", table_name="invitations")
    op.drop_index("ix_invitations_expires_at", table_name="invitations")
    op.drop_table("invitations")
