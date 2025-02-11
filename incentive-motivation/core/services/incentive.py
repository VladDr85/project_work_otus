from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.incentive import Incentive
from core.schemas.incentive import IncentiveCreate, IncentiveUpdate


async def get_incentives(session: AsyncSession) -> list[Incentive]:
    stmt = select(Incentive).order_by(Incentive.id)
    result: Result = await session.execute(stmt)
    incentives = result.scalars().all()
    return list(incentives)


async def get_incentives_by_il_id(
    session: AsyncSession,
    incentive_list_id: int,
) -> list[Incentive]:
    stmt = (
        select(Incentive)
        .where(Incentive.incentive_list_id == incentive_list_id)
        .order_by(Incentive.id)
    )
    result: Result = await session.execute(stmt)
    incentives = result.scalars().all()
    return list(incentives)


async def get_incentive(
    session: AsyncSession,
    incentive_id: int,
) -> Incentive | None:
    return await session.get(Incentive, incentive_id)


async def create_incentive(
    session: AsyncSession,
    incentive_in: IncentiveCreate,
) -> Incentive:
    incentive = Incentive(**incentive_in.model_dump())
    session.add(incentive)
    await session.commit()
    await session.refresh(incentive)
    return incentive


async def update_incentive(
    session: AsyncSession,
    incentive: Incentive,
    incentive_update: IncentiveUpdate,
) -> Incentive:
    for name, value in incentive_update.model_dump(exclude_unset=True).items():
        setattr(incentive, name, value)
    await session.commit()
    await session.refresh(incentive)
    return incentive


async def delete_incentive(
    session: AsyncSession,
    incentive: Incentive,
) -> None:
    await session.delete(incentive)
    await session.commit()
