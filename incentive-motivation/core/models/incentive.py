from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .incentive_list import IncentiveList
    from .lottery import Lottery


class Incentive(Base, IntIdPkMixin):
    """
    Описание модели ORM для объекта "Поощрение"
    """

    __tablename__ = "incentives"

    incentive_list_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("incentive_lists.id"),
        nullable=False,
    )  # ИД списка
    incentive: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )  # Наименование поощрения
    description: Mapped[str] = mapped_column(
        String(250),
        nullable=True,
    )  # Описание поощрения
    incidence_emergence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )  # Частота выпадения
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # Признак удаления

    incentive_list: Mapped["IncentiveList"] = relationship(back_populates="incentives")
    lotteries: Mapped[list["Lottery"]] = relationship(back_populates="incentive")
