import asyncio
from pathlib import Path

import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Airport, db_helper

path_to_csv = f"{Path(__file__).resolve().parent}/ru-airports.csv"


df = pd.read_csv(
    path_to_csv,
    sep=',',
).dropna(
    subset=["gps_code"]
)


async def create_airports(async_session: AsyncSession):
    async with async_session as session:
        for index, row in df.iterrows():
            new_airport = Airport(
                city=row["iso_region"],
                airport_name=row["name"],
                icao_code=row["gps_code"]
            )
            session.add(new_airport)
        await session.commit()

if __name__ == '__main__':
    asyncio.run(create_airports(db_helper.session_factory()))