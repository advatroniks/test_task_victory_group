import asyncio
from typing import Literal, Iterable

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Ticket, Flight, db_helper
from src.generate_data.tickets import utils


async def get_random_flight(
        session: AsyncSession
) -> Iterable:
    async with session as session:
        stmt = select(
            Flight
        ).order_by(
            func.random()
        )

        flight_model = await session.scalar(statement=stmt)

        available_tickets = utils.create_random_available_tickets_in_flight()

        return flight_model.flight_no, available_tickets


async def create_tickets_for_flight(
        async_session: AsyncSession,
        price: int,
        fare_condition: Literal["economy", "business", "first"],
        flight_no: str
):
    async with async_session as session:
        new_ticket = Ticket(
            price=price,
            flight_no=flight_no,
            fare_condition=fare_condition
        )
        print(new_ticket)
        session.add(new_ticket)
        await session.commit()


async def main(session: AsyncSession):
    for _ in range(100_000):
        flight_no, avail_tickets = await get_random_flight(
            session=session
        )
        for ticket in range(avail_tickets):
            fare_condition, price = utils.create_random_price_for_ticket()
            await create_tickets_for_flight(
                async_session=session,
                price=price,
                fare_condition=fare_condition,
                flight_no=flight_no
            )


if __name__ == '__main__':
    asyncio.run(main(session=db_helper.session_factory()))



