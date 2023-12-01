import asyncio
from random import randint

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Airport, Flight, db_helper
from src.generate_data.flights import utils


async def get_random_airport_icao_code(
        session: AsyncSession
):
    async with session as session:
        stmt = select(
            Airport
        ).order_by(
            func.random()
        )

        airports_models = await session.scalars(statement=stmt)

        probability = randint(1, 2)
        airports_icao_set = set()

        if probability:
            airports_icao_set.add(utils.get_random_airport())

        for airport in airports_models:
            if len(airports_icao_set) == 2:
                break
            airports_icao_set.add(airport.icao_code)

        airports_icao_list = list(airports_icao_set)
        scheduled_departure_time, scheduled_arrival_time = utils.create_random_flight_time()

        flight_model = Flight(
            flight_no=utils.create_flight_no(),
            departure_airport=airports_icao_list[0],
            arrival_airport=airports_icao_list[1],
            scheduled_departure=scheduled_departure_time,
            scheduled_arrival=scheduled_arrival_time
        )

        session.add(flight_model)
        await session.commit()


async def main():
    for i in range(10_000_000):
        try:
            await get_random_airport_icao_code(
                session=db_helper.session_factory()
            )
        except Exception:
            print(Exception)

if __name__ == '__main__':
    asyncio.run(main())
