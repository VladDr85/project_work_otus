"""create_Mission

Revision ID: 0e8de13fd5a2
Revises: 74f5f8b398a0
Create Date: 2025-02-11 11:53:27.262019

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0e8de13fd5a2"
down_revision: Union[str, None] = "74f5f8b398a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "missions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("purpose_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["purpose_id"],
            ["purposes.id"],
            name=op.f("fk_missions_purpose_id_purposes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_missions")),
    )


def downgrade() -> None:
    op.drop_table("missions")
