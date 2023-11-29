from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.database import Base


class User(Base):
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(
        String(length=30),
        unique=True,
    )

    def __str__(self):
        return f"{self.__class__.__name__} - {self.email}"

    def __repr__(self):
        return str(self)


