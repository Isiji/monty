"""initial schema"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("matches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sport", sa.String(length=30), nullable=False),
        sa.Column("provider", sa.String(length=30), nullable=False),
        sa.Column("provider_fixture_id", sa.String(length=40), nullable=True),
        sa.Column("season", sa.Integer(), nullable=True),
        sa.Column("league", sa.String(length=80), nullable=False),
        sa.Column("home_team", sa.String(length=80), nullable=False),
        sa.Column("away_team", sa.String(length=80), nullable=False),
        sa.Column("kickoff_date", sa.Date(), nullable=False),
        sa.Column("home_goals", sa.Integer(), nullable=True),
        sa.Column("away_goals", sa.Integer(), nullable=True),
        sa.UniqueConstraint("provider", "provider_fixture_id", name="uq_match_provider_fixture"),
    )
    op.create_table("api_call_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(length=30), nullable=False),
        sa.Column("endpoint", sa.String(length=80), nullable=False),
        sa.Column("called_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("api_call_logs")
    op.drop_table("matches")
