from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.types.user_id import UserIdType
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .mission import Mission
    from .user import User


class CompletedMission(Base, IntIdPkMixin):
    """
    Описание модели ORM для объекта "Журнал выполненных заданий"
    """

    __tablename__ = "completed_missions"

    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )  # ИД участника
    mission_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("missions.id", ondelete="CASCADE"),
        nullable=False,
    )  # ИД задания
    completion_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )  # Дата выполнения
    is_gave_prize: Mapped[bool] = mapped_column(
        Boolean, default=False
    )  # Признак обмена на поощрение

    user: Mapped["User"] = relationship(back_populates="completed_missions")
    mission: Mapped["Mission"] = relationship(back_populates="completed_missions")

    def __repr__(self):
        return (
            f"<CompletedMission("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"mission_id={self.mission_id}, "
            f"completion_date={self.completion_date}, "
            f"is_gave_prize={self.is_gave_prize}, "
            f")>"
        )
