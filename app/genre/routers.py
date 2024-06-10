from typing import Any

from fastapi import APIRouter, HTTPException, status

from genre.models import Genre
from genre.schemas import GenreCreateSchema, GenreSchema
from pg.repositories.entity_repository import EntityRepository
from pg.repositories.genre_repository import GenreRepository

genre_router = APIRouter()


@genre_router.post(
    '/',
    response_model=GenreSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_genres(genre: GenreCreateSchema) -> dict[str, Any]:
    EntityRepository.model = Genre

    async with EntityRepository() as repository:
        existing_genre = await repository.find_one(genre=genre.genre)

        if existing_genre is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Genre already exists')

        new_genre = await repository.add_entity({'genre': genre.genre})

    return {'id': new_genre.id, 'genre': new_genre.genre}


@genre_router.get('/', response_model=list[GenreSchema], status_code=status.HTTP_200_OK)
async def get_genres():
    async with GenreRepository() as repository:
        genres = await repository.get_genres()

    return [{'id': el.id, 'genre': el.genre, 'books': el.books} for el in genres]


@genre_router.patch('/{genre_id}', status_code=status.HTTP_200_OK)
async def update_genre(genre_id: int, data: GenreCreateSchema) -> dict[str, Any]:
    EntityRepository.model = Genre

    async with EntityRepository() as repository:
        genre = await repository.edit_one(pk=genre_id, **data.model_dump())

    return {
        'id': genre.id,
        'genre': genre.genre,
    }


@genre_router.delete('/{genre_id}', status_code=status.HTTP_200_OK)
async def delete_genre(genre_id: int):
    EntityRepository.model = Genre

    async with EntityRepository() as repository:
        await repository.delete_one(pk=genre_id)
    return {'status': True}
