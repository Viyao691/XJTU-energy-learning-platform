"""Persist conservative web model budget allocations, independent of billing."""
from alembic import op
import sqlalchemy as sa

revision = "0032"
down_revision = "0031"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "web_model_calls",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(100), nullable=False),
        sa.Column("method", sa.String(100), nullable=False),
        sa.Column("state", sa.String(40), nullable=False),
        sa.Column("reserved_cny", sa.Numeric(12, 6), nullable=False),
        sa.Column("settled_cny", sa.Numeric(12, 6), nullable=True),
        sa.Column("actual_cost_cny", sa.Numeric(12, 6), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_web_model_calls_user_id", "web_model_calls", ["user_id"])
    op.create_index("ix_web_model_calls_created_at", "web_model_calls", ["created_at"])


def downgrade():
    op.drop_table("web_model_calls")
