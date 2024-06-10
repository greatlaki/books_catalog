from typing import Any

from fastapi import APIRouter, HTTPException, status

from book.models import Book, M2MBookGenre
from book.schemas import BookCreateSchema, BookSchema
from pg.repositories.book_repository import BookRepository
from pg.repositories.entity_repository import EntityRepository

book_router = APIRouter()


@book_router.post(
    '/',
    response_model=BookSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_books(book: BookCreateSchema) -> dict[str, Any]:
    EntityRepository.model = Book

    async with EntityRepository() as repository:
        existing_book = await repository.find_one(name=book.name, author_id=book.author_id)
        if existing_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Book already exists')

        new_book = await repository.add_entity(book.model_dump())

        EntityRepository.model = M2MBookGenre
        await repository.add_entity({'book_id': new_book.id, 'genre_id': new_book.genre_id})

        return {
            'id': new_book.id,
            'name': new_book.name,
            'price': new_book.price,
            'page_count': new_book.page_count,
            'author_id': new_book.author_id,
            'genre_id': new_book.genre_id,
        }


@book_router.get('/', response_model=list[BookSchema], status_code=status.HTTP_200_OK)
async def get_books():
    async with BookRepository() as repository:
        books = await repository.get_books()

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
    EntityRepository.model = Book

    async with EntityRepository() as repository:
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
    EntityRepository.model = Book

    async with EntityRepository() as repository:
        await repository.delete_one(pk=book_id)
    return {'status': True}
