"""create_Incentive

Revision ID: 0f3001ea69b6
Revises: f88d5b33666e
Create Date: 2025-02-11 11:35:45.253807

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f3001ea69b6"
down_revision: Union[str, None] = "f88d5b33666e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "incentives",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("incentive_list_id", sa.Integer(), nullable=False),
        sa.Column("incentive", sa.String(), nullable=False),
        sa.Column("description", sa.String(length=250), nullable=True),
        sa.Column("incidence_emergence", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["incentive_list_id"],
            ["incentive_lists.id"],
            name=op.f("fk_incentives_incentive_list_id_incentive_lists"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_incentives")),
    )


def downgrade() -> None:
    op.drop_table("incentives")
