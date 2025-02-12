import random
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.lottery import Lottery
from core.models.incentive import Incentive
from core.models.incentive_list import IncentiveList
from core.schemas.lottery import LotteryCreate, LotteryUpdate


async def get_lotteries(session: AsyncSession) -> list[Lottery]:
    stmt = select(Lottery).order_by(Lottery.id)
    result: Result = await session.execute(stmt)
    lotteries = result.scalars().all()
    return list(lotteries)


async def get_lotteries_by_user_id(
    session: AsyncSession,
    user_id: int,
) -> list[Lottery]:
    stmt = select(Lottery).where(Lottery.user_id == user_id).order_by(Lottery.id)
    result: Result = await session.execute(stmt)
    lotteries = result.scalars().all()
    return list(lotteries)


async def get_lotteries_by_incentive_id(
    session: AsyncSession,
    incentive_id: int,
) -> list[Lottery]:
    stmt = (
        select(Lottery).where(Lottery.incentive_id == incentive_id).order_by(Lottery.id)
    )
    result: Result = await session.execute(stmt)
    lotteries = result.scalars().all()
    return list(lotteries)


async def get_lotteries_by_incentive_list_id(
    session: AsyncSession,
    incentive_list_id: int,
) -> list[Lottery]:
    stmt = (
        select(Lottery)
        .where(Lottery.incentive_list_id == incentive_list_id)
        .order_by(Lottery.id)
    )
    result: Result = await session.execute(stmt)
    lotteries = result.scalars().all()
    return list(lotteries)


async def get_lottery(
    session: AsyncSession,
    lottery_id: int,
) -> Lottery | None:
    return await session.get(Lottery, lottery_id)


async def create_lottery(
    session: AsyncSession,
    incentive_list_id: int,
) -> Lottery:
    # 1. Выбрать все Incentive по условию Incentive.incentive_list_id == incentive_list_id
    stmt = select(Incentive).where(Incentive.incentive_list_id == incentive_list_id)
    result: Result = await session.execute(stmt)
    incentives = result.scalars().all()

    # 2. Сохранить результат в словарь dict_incentive
    dict_incentive = {
        incentive.id: incentive.incidence_emergence for incentive in incentives
    }
    print(dict_incentive)

    # 3. Создать список, помещая в него Incentive.id столько раз, сколько указано в incidence_emergence
    incentive_list = []
    for incentive_id, incidence in dict_incentive.items():
        incentive_list.extend([incentive_id] * incidence)
    print(incentive_list)

    # 4. Выбрать одно случайное значение из incentive_list
    if not incentive_list:
        raise ValueError("Нет доступных поощрений для данного списка.")

    result_incentive_id = random.choice(incentive_list)
    print(result_incentive_id)

    # 5. Выбрать user_id из IncentiveList
    stmt = select(IncentiveList.user_id).where(IncentiveList.id == incentive_list_id)
    result: Result = await session.execute(stmt)
    result_user_id = result.scalar_one_or_none()

    if result_user_id is None:
        raise ValueError("Не удалось найти пользователя для данного списка поощрений.")

    # 6. Создать новую запись в таблице lotteries
    lottery = Lottery(
        user_id=result_user_id,
        incentive_list_id=incentive_list_id,
        incentive_id=result_incentive_id,
        # play_date=datetime.now(),
        # indication_receipt=False,
        # receipt_date=None,
    )

    session.add(lottery)
    await session.commit()
    await session.refresh(lottery)
    return lottery


async def update_lottery(
    session: AsyncSession,
    lottery: Lottery,
    lottery_update: LotteryUpdate,
) -> Lottery:
    for name, value in lottery_update.model_dump(exclude_unset=True).items():
        setattr(lottery, name, value)
    await session.commit()
    await session.refresh(lottery)
    return lottery


async def delete_lottery(
    session: AsyncSession,
    lottery: Lottery,
) -> None:
    await session.delete(lottery)
    await session.commit()


async def check_incentive_list_exists(
    session: AsyncSession, incentive_list_id: int
) -> bool:
    stmt = select(IncentiveList).where(IncentiveList.id == incentive_list_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is not None
