from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.incentive_list import IncentiveList
from core.schemas.incentive_list import IncentiveListCreate, IncentiveListUpdate


async def get_incentive_lists(session: AsyncSession) -> list[IncentiveList]:
    stmt = select(IncentiveList).order_by(IncentiveList.id)
    result: Result = await session.execute(stmt)
    incentive_lists = result.scalars().all()
    return list(incentive_lists)


async def get_incentive_list(
    session: AsyncSession,
    incentive_list_id: int,
) -> IncentiveList | None:
    return await session.get(IncentiveList, incentive_list_id)


async def create_incentive_list(
    session: AsyncSession,
    incentive_list_in: IncentiveListCreate,
) -> IncentiveList:
    incentive_lists = IncentiveList(**incentive_list_in.model_dump())
    session.add(incentive_lists)
    await session.commit()
    await session.refresh(incentive_lists)
    return incentive_lists


async def update_incentive_list(
    session: AsyncSession,
    incentive_list: IncentiveList,
    incentive_list_update: IncentiveListUpdate,
) -> IncentiveList:
    for name, value in incentive_list_update.model_dump(exclude_unset=True).items():
        setattr(incentive_list, name, value)
    await session.commit()
    await session.refresh(incentive_list)
    return incentive_list


async def delete_incentive_list(
    session: AsyncSession,
    incentive_list: IncentiveList,
) -> None:
    await session.delete(incentive_list)
    await session.commit()
