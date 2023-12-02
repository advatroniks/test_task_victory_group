from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper, Airport
from src.api_v1.tickets.exceptions import AirportNameError


async def check_airport_in_db(
        airport_departure_code: str,
        airport_arrival_code: str,
        session: AsyncSession = Depends(db_helper.get_async_session)
):
    stmt_arr = select(Airport).where(Airport.icao_code == airport_arrival_code.upper())
    stmt_dep = select(Airport).where(Airport.icao_code == airport_departure_code.upper())

    airport_model_dep = await session.scalar(statement=stmt_dep)
    if airport_model_dep:
        airport_model_arr = await session.scalar(statement=stmt_arr)
        if airport_model_arr:
            return airport_departure_code.upper(), airport_arrival_code.upper()
    else:
        raise AirportNameError

