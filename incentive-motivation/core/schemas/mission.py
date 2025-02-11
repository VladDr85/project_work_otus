from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class MissionBase(BaseModel):
    """
    Описание валидации для объекта "Список заданий"
    """

    purpose_id: Annotated[
        int,
        Field(description="ИД цели"),
    ]
    name: Annotated[
        str,
        Field(description="Наименование задания"),
    ]
    value: Annotated[
        int,
        Field(
            description="Ценность задания",
            ge=1,
            le=3,
            default=1,
        ),
    ]
    is_deleted: Annotated[
        bool,
        Field(
            description="Признак удаления",
            default=False,
        ),
    ]


class Mission(MissionBase):
    id: PositiveInt
