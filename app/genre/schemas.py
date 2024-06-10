from pydantic import BaseModel

from book.schemas import BookSchema


class GenreCreateSchema(BaseModel):
    genre: str


class GenreSchema(BaseModel):
    id: int
    genre: str
    books: list[BookSchema] = []
