from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.exceptions import EmailTaken
from src.api_v1.auth.schemas import AuthUser
from src.database import db_helper
from src.api_v1.auth import crud


async def check_unique_email(
        user_schema: AuthUser,
        session: AsyncSession = Depends(db_helper.get_async_session)
) -> AuthUser:
    if await crud.get_user_email(
        session=session,
        email=user_schema.email
    ):
        raise EmailTaken()
    return user_schema
