from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseConfig(BaseSettings):
    DB_USER: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB_PASS: str

    DB_TYPE: str = "postgresql"
    DB_DRIVER: str = "asyncpg"


db_config = DatabaseConfig()

DATABASE_URL = "%s+%s://%s:%s@%s:%s/%s" % (
    db_config.DB_TYPE,
    db_config.DB_DRIVER,
    db_config.DB_USER,
    db_config.DB_PASS,
    db_config.DB_HOST,
    db_config.DB_PORT,
    db_config.DB_NAME
)
