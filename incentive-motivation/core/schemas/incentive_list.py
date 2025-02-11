from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt, ConfigDict


class IncentiveListBase(BaseModel):
    """
    Описание валидации для объекта "Заголовок списка поощрений"
    """

    user_id: Annotated[
        int,
        Field(description="ИД участника"),
    ]
    name: Annotated[
        str,
        Field(description="Наименование списка"),
    ]
    description: Annotated[
        str,
        Field(description="Описание списка"),
    ]
    undistributed_probability: Annotated[
        int,
        Field(
            description="Не распределенная вероятность",
            ge=1,
            le=100,
            default=100,
        ),
    ]
    is_deleted: Annotated[
        bool,
        Field(
            description="Признак удаления",
            default=False,
        ),
    ]


class IncentiveListCreate(IncentiveListBase):
    pass


class IncentiveListUpdate(IncentiveListCreate):
    user_id: int | None = None
    name: str | None = None
    description: str | None = None
    undistributed_probability: int | None = None
    is_deleted: bool | None = None


class IncentiveList(IncentiveListBase):
    model_config = ConfigDict(from_attributes=True)
    id: PositiveInt
