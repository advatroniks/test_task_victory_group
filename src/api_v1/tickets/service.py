from datetime import date as datetime_date

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Flight
from src.api_v1.tickets import crud
from src.api_v1.tickets.schemas import TicketResponse
from src.api_v1.tickets.djeikstra_alg import run_algorithm
from src.api_v1.tickets.exceptions import RouteNotExist, NotAvailableTickets


async def create_response_tickets(
        session: AsyncSession,
        departure_airport: str,
        arrival_airport: str,
        date: datetime_date,
        ordered_by_time: bool | None = None,
):
    """
    Функция для создания ответа для билета. Если найден прямой билета, то возвращается он.
    Если его нет, то возвращается результат работы функции для связанных билетов.
    :param session: AsyncSession sqlalchemy obj 
    :param departure_airport: ICAO code departure airport
    :param arrival_airport:  ICAO code arrival airport
    :param date:  date ISO 8601
    :param ordered_by_time: Если указан параметр, то будет выбран самый ближний, а не самый дешевый билет.
    :return: TicketResponse | list[TicketResponse] !! в списке порядок имеет значение!!!!
    """
    flight_model = await crud.get_ticket_if_exist_direct_route(
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        date=date,
        session=session,
        ordered_by_time=ordered_by_time
    )

    if flight_model:
        return create_output_ticket_schema(
            flight_model=flight_model
        )

    return await create_combinations_tickets(
        session=session,
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        date=date
    )


def create_output_ticket_schema(
        flight_model: Flight,
):
    """
    Функция принимает объект Flight(sqlalchemy model), И превращает в схему ответа TicketResponse
    :param flight_model: Sqlalchemy model
    :return: TicketResponse pydantic schema
    :exception NotAvailableTickets если нет доступных(через relationship) билетов у рейса. 
    """
    try:
        ticket_model = flight_model.tickets[0]
    except IndexError:
        raise NotAvailableTickets

    response_schema = TicketResponse(
        departure_airport=flight_model.dep_airport_name.airport_name,
        arrival_airport=flight_model.arr_airport_name.airport_name,
        flight_no=flight_model.flight_no,
        fare_condition=ticket_model.fare_condition,
        price=ticket_model.price,
        scheduled_departure=flight_model.scheduled_departure,
        scheduled_arrival=flight_model.scheduled_arrival
    )

    return response_schema


async def create_combinations_tickets(
        session: AsyncSession,
        departure_airport: str,
        arrival_airport: str,
        date: datetime_date,
):
    """
    Функция для создания связных билетов. Создается список всех аэропортов по пути.
    Для каждой следующей пары находится билет
    :param session: AsyncSession Sqlalchemy
    :param departure_airport: Departure Airport Code
    :param arrival_airport:  Arrival Airport Code
    :param date: date ISO 8601
    :return: list[ResponseTicket pydantic obj]
    """
    route_list = await create_route_list(
        departure_airport_code=departure_airport,
        arrival_airport_code=arrival_airport,
        date=date,
        session=session
    )

    list_tickets = []
    left_cur = 0
    right_cur = left_cur + 1

    while right_cur != len(route_list[1]):
        print(route_list[1][left_cur], route_list[1][right_cur])
        flight_model = await crud.get_ticket_if_exist_direct_route(
            departure_airport=route_list[1][left_cur],
            arrival_airport=route_list[1][right_cur],
            date=date,
            session=session,
        )

        ticket_schema = create_output_ticket_schema(flight_model=flight_model)

        list_tickets.append(ticket_schema)

        left_cur += 1
        right_cur += 1

    return list_tickets


async def create_route_list(
        departure_airport_code: str,
        arrival_airport_code: str,
        date: datetime_date,
        session: AsyncSession,
):
    """
    Функция создает граф, всех перелетов их конкретного аэропорта в конкретную дату.
    Далее запускается алгоритм Дейкстры, для поиска самого дешевого связанного билета.
    :param departure_airport_code: ICAO airport departure code
    :param arrival_airport_code: ICAO airport arrival_code
    :param date: date ISO 8601
    :param session: AsyncSession Sqlalchemy obj
    :return: tuple(total_flight_price, [DepartureAirportCode, Point, ... , ArrivalAirportCode])
    :raise RouteNotExist если происходят ошибка в алгоритме поиска маршрута:
    """
    flight_dicts = await crud.get_all_directions_from_airport_by_date(
        departure_airport_code=departure_airport_code,
        date=date,
        session=session
    )

    for temp_departure_code in flight_dicts[departure_airport_code]:
        scheduled_arrival = flight_dicts[departure_airport_code][temp_departure_code][1]
        temp_dict_flights = await crud.get_all_directions_from_airport_by_date(
            departure_airport_code=temp_departure_code,
            date=date,
            session=session,
            scheduled_arrival=scheduled_arrival
        )
        if temp_dict_flights[temp_departure_code]:
            flight_dicts.update(temp_dict_flights)

    try:
        result_list = run_algorithm(
            data_dict=flight_dicts,
            dep_airport=departure_airport_code,
            arr_airport=arrival_airport_code
        )
        return result_list

    except KeyError:
        raise RouteNotExist
