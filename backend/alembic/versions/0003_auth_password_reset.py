"""add password_hash to accounts (jalon 4)
"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa

revision = "0003_auth_password_reset"
down_revision = "0002_models_core"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column("accounts", sa.Column("password_hash", sa.String(length=200), nullable=True))

def downgrade() -> None:
    op.drop_column("accounts", "password_hash")
