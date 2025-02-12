"""alter_lotteries

Revision ID: 5c00512627ab
Revises: b3a97c68f1cd
Create Date: 2025-02-12 17:59:27.270662

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5c00512627ab"
down_revision: Union[str, None] = "b3a97c68f1cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "lotteries",
        sa.Column("incentive_list_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        op.f("fk_lotteries_incentive_list_id_incentive_lists"),
        "lotteries",
        "incentive_lists",
        ["incentive_list_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_lotteries_incentive_list_id_incentive_lists"),
        "lotteries",
        type_="foreignkey",
    )
    op.drop_column("lotteries", "incentive_list_id")
