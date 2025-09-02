from alembic import op
import sqlalchemy as sa

# IDs

revision = "20250902_add_notifications"
down_revision = "0006_users_availabilities"  # ajuster a votre head precedent si different
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "notifications",
        # Utiliser String(36) pour compatibilite SQLite tests; Postgres acceptera aussi
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("channel", sa.Enum("email", "telegram", name="channel_enum"), nullable=False),
        sa.Column(
            "ntype",
            sa.Enum("invite", "reminder", "schedule_change", "cancellation", name="ntype_enum"),
            nullable=False,
        ),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("queued", "sent", "failed", name="nstatus_enum"),
            nullable=False,
            server_default="queued",
        ),
        # IMPORTANT: CURRENT_TIMESTAMP pour SQLite
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
    )
    # Index utile
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])


def downgrade():
    op.drop_index("ix_notifications_user_id", table_name="notifications")
    op.drop_table("notifications")
    # En SQLite, les Enum nommes ne creent pas de types; en Postgres, on nettoie prudemment
    try:
        op.execute("DROP TYPE IF EXISTS channel_enum")
        op.execute("DROP TYPE IF EXISTS ntype_enum")
        op.execute("DROP TYPE IF EXISTS nstatus_enum")
    except Exception:
        pass
