import uuid

from pydantic import BaseModel, EmailStr, Field


class JWTData(BaseModel):
    user_email: EmailStr = Field(alias="sub")


class AuthUser(BaseModel):
    email: EmailStr
    hashed_password: str = Field(min_length=6, max_length=50, alias="password")


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
