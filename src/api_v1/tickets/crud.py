from datetime import date as datetime_date, datetime

from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Ticket, Flight


async def get_all_directions_from_airport_by_date(
        departure_airport_code: str,
        date: datetime_date,
        session: AsyncSession,
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

    flight_scalar_result = await session.scalars(statement=stmt)

    temp_dict = {}
    for flight in flight_scalar_result:
        temp_dict[flight.arrival_airport] = flight.tickets[0].price

    result_dict = {
        departure_airport_code: temp_dict
    }

    return result_dict
