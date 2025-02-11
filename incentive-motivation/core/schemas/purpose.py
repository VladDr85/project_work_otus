from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class PurposeBase(BaseModel):
    """
    Описание валидации для объекта "Список целей мотивации"
    """

    name: Annotated[
        str,
        Field(description="Наименование цели"),
    ]
    description: Annotated[
        str,
        Field(description="Описание цели"),
    ]
    cost: Annotated[
        int,
        Field(
            description="Стоимость участия в лотереи",
            ge=3,
            le=10,
            default=3,
        ),
    ]
    is_deleted: Annotated[
        bool,
        Field(
            description="Признак удаления",
            default=False,
        ),
    ]


class Purpose(PurposeBase):
    id: PositiveInt
