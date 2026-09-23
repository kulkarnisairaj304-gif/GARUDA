"""add phishing ai fields

Revision ID: eca03a56c093
Revises:
Create Date: 2026-08-31 23:31:43.351503
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eca03a56c093"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add AI probability with a temporary default
    # so existing records can be migrated safely.
    op.add_column(
        "phishing_analyses",
        sa.Column(
            "ai_probability",
            sa.Float(),
            nullable=False,
            server_default="0",
        ),
    )

    # Add rule score with a temporary default.
    op.add_column(
        "phishing_analyses",
        sa.Column(
            "rule_score",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    # Remove the temporary database defaults.
    # New records will receive these values from the application.
    op.alter_column(
        "phishing_analyses",
        "ai_probability",
        server_default=None,
    )

    op.alter_column(
        "phishing_analyses",
        "rule_score",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "phishing_analyses",
        "rule_score",
    )

    op.drop_column(
        "phishing_analyses",
        "ai_probability",
    )