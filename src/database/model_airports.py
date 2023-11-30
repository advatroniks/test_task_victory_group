from sqlalchemy import String

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Airport(Base):
    city: Mapped[str]
    airport_name: Mapped[str]
    icao_code: Mapped[str] = mapped_column(
        String(length=4),
        primary_key=True,
        unique=True,
    )
