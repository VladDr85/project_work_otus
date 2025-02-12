from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class CompletedMissionBase(BaseModel):
    """
    Описание валидации для объекта "Журнал выполненных заданий"
    """

    user_id: Annotated[
        int,
        Field(description="ИД участника"),
    ]
    mission_id: Annotated[
        int,
        Field(description="ИД задания"),
    ]
    completion_date: Annotated[
        datetime,
        Field(
            description="Дата выполнения",
            default=datetime.now(),
        ),
    ]
    is_gave_prize: Annotated[
        bool,
        Field(
            description="Признак обмена на поощрение",
            default=False,
        ),
    ]


class CompletedMissionCreate(CompletedMissionBase):
    pass


class CompletedMission(CompletedMissionBase):
    id: PositiveInt
