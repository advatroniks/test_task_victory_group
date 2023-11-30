import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.database import Flight


class Ticket(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()")
    )
    price: Mapped[int]
    flight_no: Mapped[str] = mapped_column(
        ForeignKey("flights.flight_no")
    )
    fare_condition: Mapped[str] = mapped_column(
        String(length=10)
    )

    flight: Mapped["Flight"] = relationship(
        back_populates="tickets"
    )

    def __str__(self):
        return f"{self.__class__.__name__}-{self.flight_no}|{self.price}|{self.fare_condition}"

    def __repr__(self):
        return str(self)