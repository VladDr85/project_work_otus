from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class IncentiveBase(BaseModel):
    """
    Описание валидации для объекта "Поощрение"
    """

    incentive_list_id: Annotated[
        int,
        Field(description="ИД списка"),
    ]
    incentive: Annotated[
        str,
        Field(description="Наименование поощрения"),
    ]
    description: Annotated[
        str,
        Field(description="Описание поощрения"),
    ]
    incidence_emergence: Annotated[
        int,
        Field(
            description="Частота выпадения",
            ge=1,
            le=10,
            default=3,
        ),
    ]
    is_deleted: Annotated[
        bool,
        Field(description="Признак удаления", default=False),
    ]


class Incentive(IncentiveBase):
    id: PositiveInt
