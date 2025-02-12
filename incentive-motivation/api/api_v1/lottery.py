from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from api.api_v1.fastapi_users import (
    current_active_user,
    current_active_superuser,
)

from core.config import settings
from core.schemas.lottery import (
    Lottery,
    LotteryUpdate,
)
from core.models import db_helper, User
from core.services import lottery as lottery_service

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix=settings.api.v1.lottery,
    tags=["Результаты розыгрыша (Lottery)"],
)


@router.get(
    path="/",
    summary="Вывести результаты всех розыгрышей",
    description="Выводит все данные из объекта Lottery (История результатов розыгрыша)",
    response_model=list[Lottery],
)
async def get_lotteries(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await lottery_service.get_lotteries(session=session)


@router.get(
    path="/result-user/{user_id}/",
    summary="Все результаты розыгрыша пользователя",
    description="Вывод информации по результатам розыгрыша с фильтром по ИД пользователя Lottery.user_id (История результатов розыгрыша)",
    response_model=list[Lottery],
)
async def get_lotteries_by_user_id(
    user_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    lotteries = await lottery_service.get_lotteries_by_user_id(
        session=session,
        user_id=user_id,
    )
    if lotteries:
        return lotteries

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Lottery list {user_id} not found",
    )


@router.get(
    path="/result-incentive/{incentive_id}/",
    summary="Все результаты розыгрыша по конкретному поощрению (сколько раз выпадало)",
    description="Вывод информации по результатам розыгрыша с фильтром по ИД поощрения Lottery.incentive_id (История результатов розыгрыша)",
    response_model=list[Lottery],
)
async def get_lotteries_by_incentive_id(
    incentive_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    lotteries = await lottery_service.get_lotteries_by_incentive_id(
        session=session,
        incentive_id=incentive_id,
    )
    if lotteries:
        return lotteries

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Lottery list {incentive_id} not found",
    )


@router.get(
    path="/result-incentive_list/{incentive_list_id}/",
    summary="Все результаты розыгрыша по конкретному списку",
    description="Вывод информации по результатам розыгрыша с фильтром по ИД списка поощрения Lottery.incentive_list_id (История результатов розыгрыша)",
    response_model=list[Lottery],
)
async def get_lotteries_by_incentive_list_id(
    incentive_list_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    lotteries = await lottery_service.get_lotteries_by_incentive_list_id(
        session=session,
        incentive_list_id=incentive_list_id,
    )
    if lotteries:
        return lotteries

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Lottery list {incentive_list_id} not found",
    )


@router.get(
    path="/{lottery_id}/",
    summary="Информация по конкретному розыгрышу",
    description="Вывод информации по конкретному элементу объекта Lottery (История результатов розыгрыша)",
    response_model=Lottery,
)
async def get_lottery(
    lottery_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    incentive = await lottery_service.get_lottery(
        session=session,
        lottery_id=lottery_id,
    )
    if incentive:
        return incentive

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive {lottery_id} not found",
    )


@router.post(
    path="/add/{incentive_list_id}/",
    summary="Проведение розыгрыша лотереи",
    description="Добавляет новый элемент в объект Lottery (История результатов розыгрыша), через incentive_list_id",
    status_code=status.HTTP_201_CREATED,
    response_model=Lottery,
)
async def create_lottery(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    incentive_list_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    incentive_list_exists = await lottery_service.check_incentive_list_exists(
        session, incentive_list_id
    )
    if not incentive_list_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incentive list {incentive_list_id} not found",
        )

    return await lottery_service.create_lottery(
        session=session,
        incentive_list_id=incentive_list_id,
    )


@router.patch(
    path="/{lottery_id}/",
    summary="Обновление результатов розыгрыша (поддерживает частичное обновление)",
    description="Обновление элемента в объекте Lottery (История результатов розыгрыша)",
    response_model=Lottery,
)
async def update_lottery(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    lottery_update: LotteryUpdate,
    lottery_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    lottery = await lottery_service.get_lottery(
        session=session,
        lottery_id=lottery_id,
    )
    if lottery is not None:
        return await lottery_service.update_lottery(
            session=session,
            lottery=lottery,
            lottery_update=lottery_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive {lottery_id} not found",
    )


@router.delete(
    path="/{lottery_id}/",
    summary="Удаление результатов розыгрыша по id",
    description="Удаление элемента в объекте Lottery (История результатов розыгрыша)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_lottery(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    lottery_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> None:
    lottery = await lottery_service.get_lottery(
        session=session,
        lottery_id=lottery_id,
    )
    if lottery is not None:
        await lottery_service.delete_lottery(
            session=session,
            lottery=lottery,
        )
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive {lottery_id} not found",
    )
