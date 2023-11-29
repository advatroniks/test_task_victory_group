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

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session

    async def get_async_session(self) -> AsyncSession:
        async with self.get_scoped_session() as session:
            yield session
            await session.remove()


db_helper = DataBaseHelper(
    db_url=DATABASE_URL,
    echo=False
)


