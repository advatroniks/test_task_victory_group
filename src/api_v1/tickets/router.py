from datetime import date as datetime_date

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.api_v1.tickets.service import create_response_tickets
from src.api_v1.tickets.schemas import TicketResponse

router = APIRouter(tags=["tickets"])


@router.get(
    path="/",
    response_model=list[TicketResponse]
)
async def get_tickets(
        date: datetime_date,
        departure_airport: str,
        arrival_airport: str,
        order_by_time: bool = False,
        session: AsyncSession = Depends(db_helper.get_async_session)
):
    tickets = await create_response_tickets(
        departure_airport=departure_airport,
        arrival_airport=arrival_airport,
        date=date,
        ordered_by_time=order_by_time,
        session=session
    )

    return tickets

