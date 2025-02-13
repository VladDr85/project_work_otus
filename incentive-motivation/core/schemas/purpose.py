from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt, ConfigDict


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


class PurposeCreate(PurposeBase):
    pass


class PurposeUpdate(PurposeCreate):
    name: str | None = None
    description: str | None = None
    cost: int | None = None
    is_deleted: bool | None = None


class Purpose(PurposeBase):
    model_config = ConfigDict(from_attributes=True)
    id: PositiveInt
