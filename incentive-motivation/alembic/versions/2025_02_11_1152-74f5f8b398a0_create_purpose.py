"""create_Purpose

Revision ID: 74f5f8b398a0
Revises: 138057a3c274
Create Date: 2025-02-11 11:52:22.106504

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "74f5f8b398a0"
down_revision: Union[str, None] = "138057a3c274"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "purposes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.String(length=250), nullable=True),
        sa.Column("cost", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_purposes")),
    )


def downgrade() -> None:
    op.drop_table("purposes")
