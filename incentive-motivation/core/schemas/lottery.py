from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt


class Lottery(BaseModel):
    """
    Описание валидации для объекта "История результатов розыгрыша"
    """

    id: PositiveInt
    user_id: Annotated[
        int,
        Field(description="ИД участника"),
    ]
    incentive_id: Annotated[
        int,
        Field(description="ИД выбранного поощрения"),
    ]
    play_date: Annotated[
        datetime,
        Field(
            description="Дата проведения лотереи",
            default=datetime.now(),
        ),
    ]
    indication_receipt: Annotated[
        bool,
        Field(
            description="Признак получения",
            default=False,
        ),
    ]
    receipt_date: Annotated[
        datetime,
        Field(description="Дата получения приза"),
    ]
