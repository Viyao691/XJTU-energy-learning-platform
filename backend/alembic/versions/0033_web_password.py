"""Add optional passwords and durable password-login failure throttles."""
from alembic import op
import sqlalchemy as sa

revision = "0033"
down_revision = "0032"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("web_users", sa.Column("password_hash", sa.String(256), nullable=True))
    op.create_table(
        "web_password_failures",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email_hash", sa.String(64), nullable=False),
        sa.Column("client_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    for column in ("email_hash", "client_hash", "created_at"):
        op.create_index(f"ix_web_password_failures_{column}", "web_password_failures", [column])


def downgrade() -> None:
    op.drop_table("web_password_failures")
    op.drop_column("web_users", "password_hash")
