from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .purpose import Purpose
    from .completed_mission import CompletedMission


class Mission(Base, IntIdPkMixin):
    """
    Описание модели ORM для объекта "Список заданий"
    """

    __tablename__ = "missions"

    purpose_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "purposes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )  # ИД цели
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )  # Наименование задания
    value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )  # Ценность задания
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )  # Признак удаления

    purpose: Mapped["Purpose"] = relationship(back_populates="missions")
    completed_missions: Mapped[list["CompletedMission"]] = relationship(
        back_populates="mission"
    )

    def __repr__(self):
        return (
            f"<Mission("
            f"id={self.id}, "
            f"purpose_id={self.purpose_id}, "
            f"name={self.name}, "
            f"value={self.value}, "
            f"is_deleted={self.is_deleted}"
            f")>"
        )
