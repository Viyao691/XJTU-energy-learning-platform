"""Store visitor feedback and durable notification/rate-limit state."""
from alembic import op
import sqlalchemy as sa

revision = "0034"
down_revision = "0033"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "web_feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("web_users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("contact", sa.String(200), nullable=True),
        sa.Column("client_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("notified_at", sa.DateTime(), nullable=True),
    )
    for column in ("client_hash", "created_at"):
        op.create_index(f"ix_web_feedback_{column}", "web_feedback", [column])


def downgrade() -> None:
    op.drop_table("web_feedback")
