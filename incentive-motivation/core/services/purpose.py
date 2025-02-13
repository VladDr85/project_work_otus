from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.purpose import Purpose
from core.schemas.purpose import PurposeCreate, PurposeUpdate


async def get_purposes(session: AsyncSession) -> list[Purpose]:
    stmt = select(Purpose).order_by(Purpose.id)
    result: Result = await session.execute(stmt)
    purposes = result.scalars().all()
    return list(purposes)


async def get_purpose(
    session: AsyncSession,
    purpose_id: int,
) -> Purpose | None:
    return await session.get(Purpose, purpose_id)


async def create_purpose(
    session: AsyncSession,
    purpose_in: PurposeCreate,
) -> Purpose:
    purposes = Purpose(**purpose_in.model_dump())
    session.add(purposes)
    await session.commit()
    await session.refresh(purposes)
    return purposes


async def update_purpose(
    session: AsyncSession,
    purpose: Purpose,
    purpose_update: PurposeUpdate,
) -> Purpose:
    for name, value in purpose_update.model_dump(exclude_unset=True).items():
        setattr(purpose, name, value)
    await session.commit()
    await session.refresh(purpose)
    return purpose


async def delete_purpose(
    session: AsyncSession,
    purpose: Purpose,
) -> None:
    await session.delete(purpose)
    await session.commit()
