from datetime import date, datetime

from pydantic import BaseModel


class TicketsOptionsSchema(BaseModel):
    date: date


class TicketResponse(BaseModel):
    departure_airport: str
    arrival_airport: str
    flight_no: str
    fare_condition: str
    price: int
    scheduled_departure: datetime
    scheduled_arrival: datetime
