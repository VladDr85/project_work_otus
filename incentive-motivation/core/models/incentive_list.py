from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.user_id import UserIdType
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user import User
    from .incentive import Incentive


class IncentiveList(Base, IntIdPkMixin):
    """
    Описание модели ORM для объекта "Заголовок списка поощрений"
    """

    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )  # ИД участника
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )  # Наименование списка
    description: Mapped[str] = mapped_column(
        String(250),
        nullable=True,
    )  # Описание списка
    undistributed_probability: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )  # Не распределенная вероятность
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # Признак удаления

    user: Mapped["User"] = relationship(back_populates="incentive_lists")
    incentives: Mapped[list["Incentive"]] = relationship(
        back_populates="incentive_list"
    )

    def __repr__(self):
        return (
            f"<IncentiveList("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"name={self.name}, "
            f"description={self.description}, "
            f"undistributed_probability={self.undistributed_probability}, "
            f"is_deleted={self.is_deleted}"
            f")>"
        )
