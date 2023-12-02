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
    """
    Функция, которая запрашивает все доступные направления в указанную дату из данного аэропорта,
    Если есть хотя бы один доступный билет на данное направление.
    :param departure_airport_code:  Код аэропорта ICAO
    :param date:  Дата в формате ISO 8601
    :param session: Объект асинхронной сессии алхимии
    :param scheduled_arrival: Указание для поиска ТОЛЬКО ПОСЛЕ ЭТОГО ВРЕМЕНИ.
    :return: Возвращает словарь, где ключи - КОД АЭРОПРТА, значение list[цена:int, время прибытия:datetime]
    """
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
) -> Flight | None:
    """
    Функция для получения объекта sqlalchemy Flight. Если объект не найден, то return None
    :param session: Объект AsyncSession sqlalchemy
    :param departure_airport: код аэропорта вылета
    :param arrival_airport: код аэропорта прилета
    :param date: дата полета ISO 8601
    :param ordered_by_time: bool Если указать True, то будет найден ближайший билет.
    :return: Flight Sqlalchemy obj, если полет не найден, то None
    """
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

