from decimal import Decimal

from pg.repositories.book_repository import BookRepository, M2MBookGenreRepository

books = {
    'repository': BookRepository,
    'data': [
        {'id': 1, 'name': 'TOP 1', 'price': Decimal(500), 'page_count': 30, 'author_id': 1, 'genre_id': 3},
        {'id': 2, 'name': 'TOP 2', 'price': Decimal(400), 'page_count': 31, 'author_id': 1, 'genre_id': 2},
        {'id': 3, 'name': 'TOP 3', 'price': Decimal(300), 'page_count': 32, 'author_id': 1, 'genre_id': 1},
        {'id': 4, 'name': 'TOP 4', 'price': Decimal(200), 'page_count': 33, 'author_id': 1, 'genre_id': 1},
        {'id': 5, 'name': 'TOP 5', 'price': Decimal(100), 'page_count': 34, 'author_id': 1, 'genre_id': 3},
    ],
}

m2m_books_genres = {
    'repository': M2MBookGenreRepository,
    'data': [
        {'book_id': 1, 'genre_id': 3},
        {'book_id': 2, 'genre_id': 2},
        {'book_id': 3, 'genre_id': 1},
        {'book_id': 4, 'genre_id': 1},
        {'book_id': 5, 'genre_id': 3},
    ],
}
