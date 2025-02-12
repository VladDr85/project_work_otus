from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt, ConfigDict


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


class IncentiveCreate(IncentiveBase):
    pass


class IncentiveUpdate(IncentiveCreate):
    incentive_list_id: int | None = None
    incentive: str | None = None
    description: str | None = None
    incidence_emergence: int | None = None
    is_deleted: bool | None = None


class Incentive(IncentiveBase):
    model_config = ConfigDict(from_attributes=True)
    id: PositiveInt
