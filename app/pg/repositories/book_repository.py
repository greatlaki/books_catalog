from decimal import Decimal

from sqlalchemy import text

from base.repository import PgRepository
from book.models import Book


class BookRepository(PgRepository):
    model = Book

    async def get_books(self, filtering_data: dict[str, str | Decimal]):
        where_clause = []
        author = filtering_data['author']
        genre = filtering_data['genre']
        price__lt = filtering_data['price__lt']
        price__gte = filtering_data['price__gte']

        stmt = 'SELECT * FROM books '

        if author is not None:
            stmt += """
             JOIN
                users
            ON
                users.id = books.author_id
            """
            where_clause.append(f" CONCAT(users.first_name,' ',users.last_name) LIKE '%{author}%' ")
        if genre is not None:
            stmt += """
            JOIN
                m2m_books_genres
            ON
                m2m_books_genres.book_id = books.id
            JOIN
                genres
            ON
                genres.id = m2m_books_genres.genre_id
            """
            where_clause.append(f" genres.genre LIKE '%{genre}%' ")
        if price__lt is not None:
            where_clause.append(' price < :price__lt ')
        if price__gte is not None:
            where_clause.append(' price >= :price__gte ')

        if where_clause:
            stmt += f' WHERE {" AND ".join(where_clause)}'

        books = await self.session.execute(text(stmt), params=filtering_data)
        return books.mappings().all()
