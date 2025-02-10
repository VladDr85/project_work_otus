from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class Mission(BaseModel):
    """
    Описание валидации для объекта "Список заданий"
    """

    id: PositiveInt
    purpose_id: Annotated[int, Field(description="ИД цели")]
    name: Annotated[str, Field(description="Наименование задания")]
    value: Annotated[int, Field(description="Ценность задания", ge=1, le=3, default=1)]
    is_delete: Annotated[bool, Field(description="Признак удаления", default=False)]
