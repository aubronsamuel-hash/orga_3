"""RBAC Jalon 5: add org_memberships (account<->org with role)
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0004_rbac_org_memberships"
down_revision = "0003_auth_password_reset"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "org_memberships",
        sa.Column("id", sa.String(length=64), primary_key=True, nullable=False),
        sa.Column("org_id", sa.String(length=64), nullable=False),
        sa.Column("account_id", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),  # owner|admin|manager|tech
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
    op.create_index(
        "ix_org_memberships_org_acc",
        "org_memberships",
        ["org_id", "account_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_org_memberships_org_acc", table_name="org_memberships")
    op.drop_table("org_memberships")
