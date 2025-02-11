"""create_Lottery

Revision ID: 138057a3c274
Revises: 0f3001ea69b6
Create Date: 2025-02-11 11:36:53.843745

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "138057a3c274"
down_revision: Union[str, None] = "0f3001ea69b6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lotteries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("incentive_id", sa.Integer(), nullable=False),
        sa.Column(
            "play_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("indication_receipt", sa.Boolean(), nullable=False),
        sa.Column("receipt_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["incentive_id"],
            ["incentives.id"],
            name=op.f("fk_lotteries_incentive_id_incentives"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_lotteries_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lotteries")),
    )


def downgrade() -> None:
    op.drop_table("lotteries")
