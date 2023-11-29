from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from src.api_v1.auth.service import register_user_and_add_in_db, authenticate_user
from src.api_v1.auth.dependencies import check_unique_email
from src.api_v1.auth.schemas import AuthUser, UserResponse
from src.api_v1.auth.jwt import create_access_token
from src.database import db_helper


router = APIRouter(
    tags=["auth"]
)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def register_user(
        auth_data: AuthUser = Depends(check_unique_email),
        session: AsyncSession = Depends(db_helper.get_async_session),
):
    user = await register_user_and_add_in_db(
        session=session,
        auth_data=auth_data,
    )

    return user


@router.post(
    path="/token",
    status_code=status.HTTP_200_OK
)
async def login_for_get_access_token(
        auth_data: AuthUser,
        session: AsyncSession = Depends(db_helper.get_async_session),
) -> str:
    user = await authenticate_user(
        user_schema=auth_data,
        session=session
    )

    return create_access_token(
        user=user
    )




