from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()  # Load env variables.


class AuthConfig(BaseSettings):
    JWT_EXP: int = 60 * 60 * 24  # seconds, minutes, hours
    JWT_SECRET: str
    JWT_ALG: str


auth_config = AuthConfig()

