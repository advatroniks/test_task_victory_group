from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.api_v1.auth.schemas import AuthUser
from src.database import User


async def get_user_email(
        session: AsyncSession,
        email: str,
) -> User | None:
    stmt = select(
        User
    ).where(
        User.email == email
    )

    user_model = await session.scalar(statement=stmt)

    return user_model


async def create_user(
        session: AsyncSession,
        user_schema: AuthUser,
) -> User:
    user = User(**user_schema.model_dump())

    session.add(user)
    await session.commit()

    return user
