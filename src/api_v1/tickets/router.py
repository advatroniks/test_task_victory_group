from datetime import date as datetime_date

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.api_v1.tickets.service import create_graph_flights


router = APIRouter(tags=["tickets"])


@router.get(
    path="/"
)
async def get_tickets(
        date: datetime_date,
        departure_airport: str,
        arrival_airport: str,
        cheapest: bool = True,
        nearest: bool = False,
        session: AsyncSession = Depends(db_helper.get_async_session)
):
    return await create_graph_flights(
        session=session,
        date=date,
        departure_airport_code=departure_airport
    )
