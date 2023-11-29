from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.security import check_password, hash_password
from src.api_v1.auth.exceptions import InvalidCredentials
from src.api_v1.auth.schemas import AuthUser
from src.api_v1.auth import crud
from src.database import User


async def authenticate_user(
        user_schema: AuthUser,
        session: AsyncSession,
) -> User:
    user = await crud.get_user_email(
        session=session,
        email=user_schema.email
    )

    if not user:
        raise InvalidCredentials()

    if not check_password(
        plain_password=user_schema.hashed_password,  # field hashed password in pydantic it's PLAIN PASSWORD!!!
        hashed_password=user.hashed_password
    ):
        raise InvalidCredentials()

    return user


async def register_user_and_add_in_db(
        session: AsyncSession,
        auth_data: AuthUser,
):
    auth_data.hashed_password = hash_password(auth_data.hashed_password)
    new_user = User(**auth_data.model_dump())

    session.add(new_user)
    await session.commit()

    return new_user
