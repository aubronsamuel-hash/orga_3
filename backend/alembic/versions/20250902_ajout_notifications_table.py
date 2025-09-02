from alembic import op
import sqlalchemy as sa

revision = "20250902_ajout_notifications_table"
down_revision = "0006_users_availabilities"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "notifications",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel", sa.Enum("email", "telegram", name="channel_enum"), nullable=False),
        sa.Column(
            "ntype",
            sa.Enum(
                "invite",
                "reminder",
                "schedule_change",
                "cancellation",
                name="ntype_enum",
            ),
            nullable=False,
        ),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("queued", "sent", "failed", name="nstatus_enum"),
            nullable=False,
            server_default="queued",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")
    op.execute("DROP TYPE IF EXISTS channel_enum")
    op.execute("DROP TYPE IF EXISTS ntype_enum")
    op.execute("DROP TYPE IF EXISTS nstatus_enum")
