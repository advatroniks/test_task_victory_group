import uuid

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Ticket(Base):
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=uuid.UUID,
        server_default=text("uuid_generate_v4()")
    )
    price: Mapped[int]
    flight_no: Mapped[str] = mapped_column(
        ForeignKey("flights.flight_no")
    )
    fare_conditions: Mapped[str] = mapped_column(
        String(length=10)
    )
