from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.exceptions import EmailTaken
from src.api_v1.auth.schemas import AuthUser
from src.api_v1.auth import crud


async def check_unique_email(
        session: AsyncSession,
        user_schema: AuthUser,
) -> AuthUser:
    if not await crud.get_user_email(
        session=session,
        email=user_schema.email
    ):
        raise EmailTaken()

    return user_schema
