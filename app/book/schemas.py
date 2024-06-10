from decimal import Decimal

from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    page_count: int | None = None
    author_id: int | None = None
    genre_id: int | None = None


class BookSchema(BaseModel):
    id: int
    name: str
    price: Decimal
    page_count: int
    author_id: int
    genre_id: int
