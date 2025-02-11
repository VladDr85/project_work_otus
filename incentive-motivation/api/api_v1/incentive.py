from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from api.api_v1.fastapi_users import (
    current_active_user,
    current_active_superuser,
)

from core.config import settings
from core.schemas.incentive import (
    Incentive,
    IncentiveCreate,
    IncentiveUpdate,
)
from core.models import db_helper, User
from core.services import incentive as incentive_service

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix=settings.api.v1.incentive,
    tags=["Поощрения (Incentive)"],
)


@router.get(
    path="/",
    summary="Вывести все поощрения",
    description="Выводит все данные из объекта Incentive (Поощрения)",
    response_model=list[Incentive],
)
async def get_incentives(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await incentive_service.get_incentives(session=session)


@router.get(
    path="/list/{incentive_list_id}/",
    summary="Все поощрения в для розыгрыша",
    description="Вывод информации по поощрениям с фильтром по ИД заголовка Incentive.incentive_list_id (Поощрения)",
    response_model=list[Incentive],
)
async def get_incentives_by_il_id(
    incentive_list_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    incentive_list = await incentive_service.get_incentives_by_il_id(
        session=session,
        incentive_list_id=incentive_list_id,
    )
    if incentive_list:
        return incentive_list

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive list {incentive_list_id} not found",
    )


@router.get(
    path="/{incentive_id}/",
    summary="Информация по конкретному поощрению",
    description="Вывод информации по конкретному элементу объекта Incentive (Поощрения)",
    response_model=Incentive,
)
async def get_incentive(
    incentive_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    incentive = await incentive_service.get_incentive(
        session=session,
        incentive_id=incentive_id,
    )
    if incentive:
        return incentive

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive {incentive_id} not found",
    )


@router.post(
    path="/",
    summary="Добавление нового поощрения",
    description="Добавляет новый элемент в объект Incentive (Поощрения)",
    status_code=status.HTTP_201_CREATED,
    response_model=Incentive,
)
async def create_incentive(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    incentive_in: IncentiveCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await incentive_service.create_incentive(
        session=session,
        incentive_in=incentive_in,
    )


@router.patch(
    path="/{incentive_id}/",
    summary="Обновление поощрения (поддерживает частичное обновление)",
    description="Обновление элемента в объекте Incentive (Поощрения)",
    response_model=Incentive,
)
async def update_incentive(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    incentive_update: IncentiveUpdate,
    incentive_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    incentive = await incentive_service.get_incentive(
        session=session,
        incentive_id=incentive_id,
    )
    if incentive is not None:
        return await incentive_service.update_incentive(
            session=session,
            incentive=incentive,
            incentive_update=incentive_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive {incentive_id} not found",
    )


@router.delete(
    path="/{incentive_id}/",
    summary="Удаление поощрения по id",
    description="Удаление элемента в объекте Incentive (Поощрения)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_incentive(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    incentive_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> None:
    incentive = await incentive_service.get_incentive(
        session=session,
        incentive_id=incentive_id,
    )
    if incentive is not None:
        await incentive_service.delete_incentive(
            session=session,
            incentive=incentive,
        )
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive {incentive_id} not found",
    )
