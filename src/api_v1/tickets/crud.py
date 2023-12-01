from datetime import date as datetime_date

from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Flight


async def get_all_directions_from_airport_by_date(
        departure_airport_code: str,
        date: datetime_date,
        session: AsyncSession,
        scheduled_arrival: datetime_date | None = None,
) -> dict:
    stmt = (select(
        Flight
     ).options(
        selectinload(Flight.tickets)
     ).where(
        and_(
            Flight.tickets.any(),
            func.date(Flight.scheduled_departure) == date,
            Flight.departure_airport == departure_airport_code,
        )
     )
    )

    if scheduled_arrival:
        stmt = stmt.where(
            Flight.scheduled_departure > scheduled_arrival
        )

    flight_scalar_result = await session.scalars(statement=stmt)

    temp_dict = {}
    for flight in flight_scalar_result:
        temp_dict[flight.arrival_airport] = [flight.tickets[0].price, flight.scheduled_arrival]

    result_dict = {
        departure_airport_code: temp_dict
    }

    return result_dict
