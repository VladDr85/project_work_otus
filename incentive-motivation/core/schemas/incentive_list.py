from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


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


class IncentiveList(IncentiveListBase):
    id: PositiveInt
