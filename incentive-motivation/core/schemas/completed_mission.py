from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class CompletedMission(BaseModel):
    """
    Описание валидации для объекта "Журнал выполненных заданий"
    """

    id: PositiveInt
    user_id: Annotated[int, Field(description="ИД участника")]
    mission_id: Annotated[int, Field(description="ИД задания")]
    completion_date: Annotated[
        datetime, Field(description="Дата выполнения", default=datetime.now())
    ]
    is_delete: Annotated[bool, Field(description="Признак удаления", default=False)]
