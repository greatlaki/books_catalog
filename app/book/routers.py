from decimal import Decimal
from typing import Any

from fastapi import APIRouter, HTTPException, status

from book.models import Book, M2MBookGenre
from book.schemas import BookCreateSchema, BookSchema
from database.uow import PgUow
from pg.repositories.book_repository import BookRepository
from pg.repositories.entity_repository import EntityRepository

book_router = APIRouter()


@book_router.post(
    '/',
    response_model=BookSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_books(book: BookCreateSchema) -> dict[str, Any]:
    async with PgUow() as uow:
        book_repo = EntityRepository(Book, uow)
        m2m_repo = EntityRepository(M2MBookGenre, uow)

        existing_book = await book_repo.find_one(name=book.name, author_id=book.author_id)
        if existing_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book already exists')

        new_book = await book_repo.add_entity(book.model_dump())

        await m2m_repo.add_entity({'book_id': new_book.id, 'genre_id': new_book.genre_id})

        return {
            'id': new_book.id,
            'name': new_book.name,
            'price': new_book.price,
            'page_count': new_book.page_count,
            'author_id': new_book.author_id,
            'genre_id': new_book.genre_id,
        }


@book_router.get('/', response_model=list[BookSchema], status_code=status.HTTP_200_OK)
async def get_books(
    author: str | None = None,
    genre: str | None = None,
    price__lt: Decimal | None = None,
    price__gte: Decimal | None = None,
):
    if author.isdigit() or genre.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Author or genre should be a string')

    filtering_by = {'author': author, 'genre': genre, 'price__lt': price__lt, 'price__gte': price__gte}

    async with BookRepository() as repository:
        books = await repository.get_books(filtering_by)

    return [
        {
            'id': el.id,
            'name': el.name,
            'price': el.price,
            'page_count': el.page_count,
            'author_id': el.author_id,
            'genre_id': el.genre_id,
        }
        for el in books
    ]


@book_router.patch('/{book_id}', status_code=status.HTTP_200_OK)
async def update_book(book_id: int, data: BookCreateSchema) -> dict[str, Any]:
    async with EntityRepository(Book) as repository:
        book = await repository.edit_one(pk=book_id, **data.model_dump(exclude_none=True))

    return {
        'id': book.id,
        'name': book.name,
        'price': book.price,
        'page_count': book.page_count,
        'author_id': book.author_id,
        'genre_id': book.genre_id,
    }


@book_router.delete('/{book_id}', status_code=status.HTTP_200_OK)
async def delete_book(book_id: int):
    async with EntityRepository(Book) as repository:
        await repository.delete_one(pk=book_id)
    return {'status': True}
