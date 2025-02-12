from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.user_id import UserIdType
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .incentive import Incentive
    from .incentive_list import IncentiveList
    from .user import User


class Lottery(Base, IntIdPkMixin):
    """
    Описание модели ORM для объекта "История результатов розыгрыша"
    """

    __tablename__ = "lotteries"

    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )  # ИД участника
    incentive_list_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("incentive_lists.id"),
        nullable=False,
    )  # ИД списка
    incentive_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("incentives.id", ondelete="CASCADE"),
        nullable=False,
    )  # ИД выбранного поощрения
    play_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )  # Дата проведения лотереи
    indication_receipt: Mapped[bool] = mapped_column(
        Boolean, default=False
    )  # Признак получения
    receipt_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )  # Дата получения приза

    user: Mapped["User"] = relationship(back_populates="lotteries")
    incentive_list: Mapped["IncentiveList"] = relationship(back_populates="lotteries")
    incentive: Mapped["Incentive"] = relationship(back_populates="lotteries")

    def __repr__(self):
        return (
            f"<Lottery("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"incentive_id={self.incentive_id}, "
            f"play_date={self.play_date}, "
            f"indication_receipt={self.indication_receipt}, "
            f"receipt_date={self.receipt_date}, "
            f")>"
        )
