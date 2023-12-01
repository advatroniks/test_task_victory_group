from datetime import date as datetime_date

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.tickets import crud


async def create_graph_flights(
        departure_airport_code: str,
        date: datetime_date,
        session: AsyncSession,
):
    flight_models = await crud.get_all_directions_from_airport_by_date(
        departure_airport_code=departure_airport_code,
        date=date,
        session=session
    )

    for temp_departure_code in flight_models[departure_airport_code]:
        scheduled_arrival = flight_models[departure_airport_code][temp_departure_code][1]
        temp_dict_flights = await crud.get_all_directions_from_airport_by_date(
            departure_airport_code=temp_departure_code,
            date=date,
            session=session,
            scheduled_arrival=scheduled_arrival
        )
        if temp_dict_flights[temp_departure_code]:
            flight_models.update(temp_dict_flights)

    return flight_models
