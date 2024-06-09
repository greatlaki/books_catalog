import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from settings import settings

logger = logging.getLogger('app')


class Engines(object):
    pg_async_engine: AsyncEngine
    pg_async_session_maker: async_sessionmaker[AsyncSession]

    def __init__(self) -> None:
        self.make_connect()

    def make_connect(self):
        self.pg_async_engine = create_async_engine(
            settings.PG.ADDRESS,
            pool_size=50,
            max_overflow=5,
            pool_pre_ping=True,
            isolation_level='REPEATABLE READ',
        )

        self.pg_async_session_maker = async_sessionmaker(self.pg_async_engine, expire_on_commit=False)

    async def engines_dispose(self):
        await self.pg_async_engine.dispose()

    async def test_connect(self):
        async def check_pg_connection():
            async with self.pg_async_engine.connect() as conn:
                result = await conn.execute(text('SELECT version()'))
                logger.info(f'catalog pg async info: {result.scalars().one()}')

        await check_pg_connection()


engines = Engines()
