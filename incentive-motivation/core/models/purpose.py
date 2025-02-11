from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .mission import Mission


class Purpose(Base, IntIdPkMixin):
    """
    Описание модели ORM для объекта "Список целей мотивации"
    """

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )  # Наименование цели
    description: Mapped[str] = mapped_column(
        String(250),
        nullable=True,
    )  # Описание цели
    cost: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )  # Стоимость участия в лотереи
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # Признак удаления

    missions: Mapped[list["Mission"]] = relationship(back_populates="purpose")

    def __repr__(self):
        return (
            f"<Purpose("
            f"id={self.id}, "
            f"name={self.name}, "
            f"cost={self.cost}, "
            f"is_deleted={self.is_deleted}"
            f")>"
        )
