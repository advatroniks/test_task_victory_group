from datetime import date as datetime_date

from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload, joinedload, join

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Flight, Ticket


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


async def get_ticket_if_exist_direct_route(
        session: AsyncSession,
        departure_airport: str,
        arrival_airport: str,
        date: datetime_date,
        ordered_by_time: bool | None = None,
):
    stmt = select(
        Flight
    ).options(
        joinedload(Flight.tickets),
        joinedload(Flight.arr_airport_name),
        joinedload(Flight.dep_airport_name)
    ).where(
        and_(
            Flight.departure_airport == departure_airport,
            Flight.arrival_airport == arrival_airport,
            func.date(Flight.scheduled_departure) == date,
        )
    )

    if ordered_by_time:
        stmt = stmt.order_by(Flight.scheduled_departure.asc())

    flight = await session.scalar(statement=stmt)

    if not flight:
        return None

    return flight

