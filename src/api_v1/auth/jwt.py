from datetime import datetime, timedelta

from jose import JWTError, jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from src.api_v1.auth.exceptions import InvalidToken, AuthRequired
from src.api_v1.auth.config import auth_config
from src.api_v1.auth.schemas import JWTData
from src.database import User


auth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/token")


def create_access_token(
        user: User,
        expires_delta=timedelta(seconds=auth_config.JWT_EXP)
):
    jwt_data = {
        "sub": user.email,
        "exp": datetime.utcnow() + expires_delta
    }

    return jwt.encode(
        claims=jwt_data,
        key=auth_config.JWT_SECRET,
        algorithm=auth_config.JWT_ALG
    )


async def parse_jwt_data(
        token: str = Depends(auth2_scheme)
):
    try:
        payload = jwt.decode(
            token=token,
            key=auth_config.JWT_SECRET,
            algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        raise InvalidToken

    JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_data),
) -> JWTData:
    """
    Принимает access_token(JWTData pydantic Schema) проверяет
    существование и возвращает access_token (JWTData pycantic schema)
    :param token: JWTData данные из access token(pydantic schema)
    :return: JWTData pydantic Schema
    :exception AuthRequired: Если JWTData is None
    """
    if not token:
        raise AuthRequired()

    return token
