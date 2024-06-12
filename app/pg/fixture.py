import logging
from typing import Any

from pydantic import BaseModel, ValidationError

from base.repository import PgRepository
from pg.fixtures.book_fixture import books, m2m_books_genres
from pg.fixtures.genre_fixture import genres
from pg.fixtures.user_fixture import users

logger = logging.getLogger('app')


class FixtureData(BaseModel):
    repository: type[PgRepository]
    data: list[dict[str, Any]]


class DatabaseFixtures:
    fixtures = [genres, users, books, m2m_books_genres]

    async def load_data(self, data: FixtureData):
        try:
            async with data.repository() as repository:
                await repository.load_fixture_data(data.data)

        except Exception as ex:
            logger.error(msg=f'{data.repository.model.__tablename__} not loaded', extra={'exception': ex})

    async def run(self):
        logger.info(msg='Start loading fixtures')

        for fixture in self.fixtures:
            try:
                await self.load_data(FixtureData.model_validate(fixture))

            except ValidationError as ex:
                logger.error(msg='Fixture validation error', extra={'exception': ex})

        logger.info(msg='Fixtures has been load')
