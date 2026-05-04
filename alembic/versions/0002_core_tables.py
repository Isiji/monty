"""core tables"""
from alembic import op
import sqlalchemy as sa

revision = "0002_core_tables"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("team_match_stats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("match_id", sa.Integer(), sa.ForeignKey("matches.id"), nullable=False),
        sa.Column("team", sa.String(length=80), nullable=False),
        sa.Column("is_home", sa.Integer(), nullable=False),
        sa.Column("goals", sa.Integer(), nullable=False),
        sa.Column("corners", sa.Integer(), nullable=False),
        sa.Column("shots_on_target", sa.Integer(), nullable=False),
        sa.Column("possession", sa.Float(), nullable=False),
        sa.Column("fouls", sa.Integer(), nullable=False),
        sa.Column("cards", sa.Integer(), nullable=False),
        sa.Column("keeper_saves", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("team_match_stats")
