from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, status

from src.api_v1.auth.dependencies import check_unique_email
from src.api_v1.auth.schemas import AuthUser, UserResponse
from src.api_v1.auth.service import authenticate_user
from src.api_v1.auth.jwt import create_access_token
from src.database import db_helper
from src.api_v1.auth import crud


router = APIRouter(
    tags=["auth"]
)


@router.post(
    path="/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
        session: AsyncSession = Depends(db_helper.get_async_session),
        auth_data: AuthUser = Depends(check_unique_email),
):
    user = await crud.create_user(
        session=session,
        user_schema=auth_data,
    )

    return user


@router.get(
    path="/tokens"
)
async def login_for_get_access_token(
        auth_data: AuthUser,
        session: AsyncSession = Depends(db_helper.get_async_session),
):
    user = await authenticate_user(
        user_schema=auth_data,
        session=session
    )

    return create_access_token(
        user=user
    )



