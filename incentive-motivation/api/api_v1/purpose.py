from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from api.api_v1.fastapi_users import (
    current_active_user,
    current_active_superuser,
)

from core.config import settings
from core.schemas.purpose import (
    Purpose,
    PurposeCreate,
    PurposeUpdate,
)
from core.models import db_helper, User
from core.services import purpose as purpose_service

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import User


router = APIRouter(
    prefix=settings.api.v1.purpose,
    tags=["Список целей мотивации (Purpose)"],
)


@router.get(
    path="/",
    summary="Вывести все цели по мотивации",
    description="Выводит все данные из объекта Purpose (Список целей мотивации)",
    response_model=list[Purpose],
)
async def get_purposes(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await purpose_service.get_purposes(session=session)


@router.get(
    path="/{purpose_id}/",
    summary="Информация по конкретной цели",
    description="Вывод информации по конкретному элементу объекта Purpose (Список целей мотивации)",
    response_model=Purpose,
)
async def get_purpose(
    purpose_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    purpose = await purpose_service.get_purpose(
        session=session,
        purpose_id=purpose_id,
    )
    if purpose is not None:
        return purpose

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Purpose {purpose_id} not found",
    )


@router.post(
    path="/",
    summary="Добавление новой цели",
    description="Добавляет новый элемент в объект Purpose (Список целей мотивации)",
    response_model=Purpose,
    status_code=status.HTTP_201_CREATED,
)
async def create_purpose(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    purpose_in: PurposeCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    return await purpose_service.create_purpose(
        session=session,
        purpose_in=purpose_in,
    )


@router.patch(
    path="/{purpose_id}/",
    summary="Обновление цели (поддерживает частичное обновление)",
    description="Обновление элемента в объекте Purpose (Список целей мотивации)",
    response_model=Purpose,
)
async def update_purpose(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    purpose_update: PurposeUpdate,
    purpose_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    purpose = await purpose_service.get_purpose(
        session=session,
        purpose_id=purpose_id,
    )
    if purpose is not None:
        return await purpose_service.update_purpose(
            session=session,
            purpose=purpose,
            purpose_update=purpose_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Purpose {purpose_id} not found",
    )


@router.delete(
    path="/{purpose_id}/",
    summary="Удаление цели мотивации по id",
    description="Удаление элемента в объекте Purpose (Список целей мотивации)",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_purpose(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
    purpose_id: int,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
) -> None:
    purpose = await purpose_service.get_purpose(
        session=session,
        purpose_id=purpose_id,
    )
    if purpose is not None:
        await purpose_service.delete_purpose(
            session=session,
            purpose=purpose,
        )
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Purpose {purpose_id} not found",
    )
