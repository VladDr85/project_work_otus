from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from api.api_v1.fastapi_users import (
    current_active_user,
    current_active_superuser,
)

from core.config import settings
from core.schemas.incentive_list import (
    IncentiveList,
    IncentiveListCreate,
    IncentiveListUpdate,
)
from core.models import db_helper, User
from core.services import incentive_list as incentive_list_service
from core.services.incentive import get_sum_incidence_emergence

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import User


router = APIRouter(
    prefix=settings.api.v1.incentive_lists,
    tags=["Заголовок списка поощрений (IncentiveList)"],
)


@router.get(
    path="/",
    summary="Вывести все заголовки поощрений",
    description="Выводит все данные из объекта IncentiveList (Заголовок списка поощрений)",
    response_model=list[IncentiveList],
)
async def get_incentive_lists(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await incentive_list_service.get_incentive_lists(session=session)


@router.get(
    path="/{incentive_list_id}/",
    summary="Информация по конкретному заголовку поощрения",
    description="Вывод информации по конкретному элементу объекта IncentiveList (Заголовок списка поощрений)",
    response_model=IncentiveList,
)
async def get_incentive_list(
    incentive_list_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    incentive_list = await incentive_list_service.get_incentive_list(
        session=session,
        incentive_list_id=incentive_list_id,
    )
    if incentive_list is not None:
        return incentive_list

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive list {incentive_list_id} not found",
    )


@router.post(
    path="/",
    summary="Добавление нового заголовка поощрений",
    description="Добавляет новый элемент в объект IncentiveList (Заголовок списка поощрений)",
    response_model=IncentiveList,
    status_code=status.HTTP_201_CREATED,
)
async def create_incentive_list(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    incentive_list_in: IncentiveListCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await incentive_list_service.create_incentive_list(
        session=session,
        incentive_list_in=incentive_list_in,
    )


@router.patch(
    path="/{incentive_list_id}/",
    summary="Обновление заголовка поощрений (поддерживает частичное обновление)",
    description="Обновление элемента в объекте IncentiveList (Заголовок списка поощрений)",
    response_model=IncentiveList,
)
async def update_incentive_list(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    incentive_list_update: IncentiveListUpdate,
    incentive_list_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    incentive_list = await incentive_list_service.get_incentive_list(
        session=session,
        incentive_list_id=incentive_list_id,
    )
    if incentive_list is not None:
        return await incentive_list_service.update_incentive_list(
            session=session,
            incentive_list=incentive_list,
            incentive_list_update=incentive_list_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive list {incentive_list_id} not found",
    )


@router.patch(
    path="/undistributed-probability/{incentive_list_id}",
    summary="Обновление поля undistributed_probability",
    description="Обновляет поле undistributed_probability значением, полученным из суммы incidence_emergence",
    response_model=IncentiveList,
)
async def update_undistributed_probability(
    incentive_list_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    sum_incidence_emergence = await get_sum_incidence_emergence(
        session=session,
        incentive_list_id=incentive_list_id,
    )

    incentive_list = await incentive_list_service.get_incentive_list(
        session=session,
        incentive_list_id=incentive_list_id,
    )

    if incentive_list is not None:
        incentive_list.undistributed_probability = sum_incidence_emergence
        return await incentive_list_service.update_incentive_list(
            session=session,
            incentive_list=incentive_list,
            incentive_list_update=IncentiveListUpdate(
                undistributed_probability=100 - sum_incidence_emergence
            ),
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive list {incentive_list_id} not found",
    )


@router.delete(
    path="/{incentive_list_id}/",
    summary="Удаление заголовка поощрений по id",
    description="Удаление элемента в объекте IncentiveList (Заголовок списка поощрений)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_incentive_list(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    incentive_list_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> None:
    incentive_list = await incentive_list_service.get_incentive_list(
        session=session,
        incentive_list_id=incentive_list_id,
    )
    if incentive_list is not None:
        await incentive_list_service.delete_incentive_list(
            session=session,
            incentive_list=incentive_list,
        )
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Incentive list {incentive_list_id} not found",
    )
