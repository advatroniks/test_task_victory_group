from datetime import date as datetime_date

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.api_v1.tickets import crud



router = APIRouter(tags=["tickets"])


@router.get(
    path="/"
)
async def get_tickets(
        date: datetime_date,
        departure_airport: str,
        arrival_airport: str,
        session: AsyncSession = Depends(db_helper.get_async_session)
):
    return await crud.get_all_directions_from_airport_by_date(
        session=session,
        date=date,
        airport_icao_code=departure_airport
    )
