from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt, ConfigDict


class LotteryBase(BaseModel):
    """
    Описание валидации для объекта "История результатов розыгрыша"
    """

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


class LotteryCreate(LotteryBase):
    pass


class LotteryUpdate(LotteryCreate):
    user_id: int | None = None
    incentive_id: int | None = None
    play_date: datetime | None = None
    indication_receipt: bool | None = None
    receipt_date: datetime | None = None


class Lottery(LotteryBase):
    model_config = ConfigDict(from_attributes=True)
    id: PositiveInt
