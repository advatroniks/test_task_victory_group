import uuid

from sqlalchemy import String, text, Uuid as Uuid_sql
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class User(Base):
    id: Mapped[str] = mapped_column(
        Uuid_sql,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
        primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=30),
        unique=True,
    )
    hashed_password: Mapped[str]

    def __str__(self):
        return f"{self.__class__.__name__} - {self.email}"

    def __repr__(self):
        return str(self)


