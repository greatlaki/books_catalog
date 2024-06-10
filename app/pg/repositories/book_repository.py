from sqlalchemy import select

from base.repository import PgRepository
from book.models import Book


class BookRepository(PgRepository):
    model = Book

    async def get_books(self):
        stmt = select(self.model)
        genres = await self.session.execute(stmt)
        return genres.mappings().all()
