from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.database import Ticket


class Flight(Base):
    __table_args__ = (
        CheckConstraint(
            "departure_airport != arrival_airport",
            name="check airport value",
        ),
    )

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

    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="flight",
        order_by="asc(Ticket.price)"
    )

    def __str__(self):
        return f"{self.__class__.__name__}:{self.departure_airport}>>{self.arrival_airport}"

    def __repr__(self):
        return str(self)