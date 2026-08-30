"""add fndds page field to global constant

Revision ID: 02c0f746e145
Revises: 61e021f47bdb
Create Date: 2026-08-30 17:43:03.494894

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "02c0f746e145"
down_revision: str | Sequence[str] | None = "61e021f47bdb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "global_constants",
        "current_usda_food_page",
        new_column_name="current_foundation_food_page",
    )

    op.add_column(
        "global_constants",
        sa.Column(
            "current_fndds_food_page",
            sa.Integer(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "global_constants",
        "current_fndds_food_page",
    )

    op.alter_column(
        "global_constants",
        "current_foundation_food_page",
        new_column_name="current_usda_food_page",
    )
