from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class Incentive(BaseModel):
    """
    Описание валидации для объекта "Поощрение"
    """

    id: PositiveInt
    incentive_list_id: Annotated[int, Field(description="ИД списка")]
    incentive: Annotated[str, Field(description="Наименование поощрения")]
    description: Annotated[str, Field(description="Описание")]
    incidence_emergence: Annotated[
        int, Field(description="Частота выпадения", ge=1, le=10, default=3)
    ]
    is_delete: Annotated[bool, Field(description="Признак удаления", default=False)]
