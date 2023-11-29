import uuid
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from sqlalchemy import text, Uuid as Uuid_sql


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id: Mapped[str] = mapped_column(
        Uuid_sql,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
        primary_key=True
    )

