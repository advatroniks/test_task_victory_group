from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Flight(Base):
    flight_no: Mapped[str] = mapped_column(
        String(length=7),
        primary_key=True,
        unique=True
    )
    departure_airport: Mapped[str] = mapped_column(
        ForeignKey("airports.icao_code")
    )
    arrival_airport: Mapped[str] = mapped_column(
        ForeignKey("airports.icao_code")
    )
    scheduled_departure: Mapped[datetime]
    scheduled_arrival: Mapped[datetime]




