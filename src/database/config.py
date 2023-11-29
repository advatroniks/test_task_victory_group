from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session

from src.config import DATABASE_URL


class DataBaseHelper:
    def __init__(
            self,
            db_url: str,
            echo: bool = False  # For debug mode set echo = True
    ):
        self.engine = create_async_engine(
            url=db_url,
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def get_async_session(self):
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DataBaseHelper(
    db_url=DATABASE_URL,
    echo=False
)


