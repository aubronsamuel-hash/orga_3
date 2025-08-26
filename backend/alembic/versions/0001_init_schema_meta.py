"""init schema_meta minimal jalon 2
"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa

# Revision identifiers

revision = "0001_init_schema_meta"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "schema_meta",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("key", sa.String(length=64), nullable=False, unique=True),
        sa.Column("value", sa.String(length=256), nullable=False),
    )
    op.create_index("ix_schema_meta_key", "schema_meta", ["key"], unique=True)

def downgrade() -> None:
    op.drop_index("ix_schema_meta_key", table_name="schema_meta")
    op.drop_table("schema_meta")
