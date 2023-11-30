from datetime import date as datetime_date, datetime

from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Ticket, Flight


async def get_all_directions_from_airport_by_date(
        airport_icao_code: str,
        date: datetime_date,
        session: AsyncSession,
):
    stmt = (select(
        Flight
     ).options(
        selectinload(Flight.tickets)
     ).where(
        and_(
            Flight.tickets.any(),
            func.date(Flight.scheduled_departure) == date,
            Flight.departure_airport == airport_icao_code,
        )
     )
    )

    result = await session.scalars(statement=stmt)

    total = ""
    for flight in result:
        total = f"{flight}, {flight.tickets[0]}"

    return total
