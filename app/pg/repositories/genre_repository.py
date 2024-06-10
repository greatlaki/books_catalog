from sqlalchemy import select
from sqlalchemy.orm import selectinload

from base.repository import PgRepository
from genre.models import Genre


class GenreRepository(PgRepository):
    model = Genre

    async def get_genres(self):
        stmt = select(self.model).options(selectinload(self.model.books))
        genres = await self.session.execute(stmt)
        return genres.scalars().all()
