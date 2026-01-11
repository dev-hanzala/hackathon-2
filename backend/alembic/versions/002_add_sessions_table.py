"""Add sessions table for Better Auth integration.

Revision ID: 002
Revises: 001
Create Date: 2026-01-11 12:00:00.000000

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sessions table for Better Auth
    op.create_table(
        "session",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token", sa.String(512), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index("idx_session_user_id", "session", ["user_id"])
    op.create_index("idx_session_token", "session", ["token"], unique=True)
    op.create_index("idx_session_expires_at", "session", ["expires_at"])


def downgrade() -> None:
    op.drop_index("idx_session_expires_at", table_name="session")
    op.drop_index("idx_session_token", table_name="session")
    op.drop_index("idx_session_user_id", table_name="session")
    op.drop_table("session")
