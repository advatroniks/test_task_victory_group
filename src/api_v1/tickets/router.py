from datetime import date as datetime_date

from fastapi import APIRouter, Depends, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import db_helper
from src.api_v1.tickets.service import create_response_tickets
from src.api_v1.tickets.schemas import TicketResponse
from src.api_v1.tickets.dependencies import check_airport_in_db
from src.api_v1.auth.jwt import parse_jwt_user_data

router = APIRouter(tags=["tickets"])


@router.get(
    path="/",
    response_model=list[TicketResponse],
    status_code=status.HTTP_202_ACCEPTED
)
async def get_tickets(
        date: datetime_date,
        order_by_time: bool = False,
        departure_arrival_airports_list: str = Depends(check_airport_in_db),
        session: AsyncSession = Depends(db_helper.get_async_session),
        current_user=Depends(parse_jwt_user_data),
):

    tickets = await create_response_tickets(
        departure_airport=departure_arrival_airports_list[0],
        arrival_airport=departure_arrival_airports_list[1],
        date=date,
        ordered_by_time=order_by_time,
        session=session
    )

    return tickets

