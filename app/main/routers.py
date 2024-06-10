from fastapi import APIRouter

from book.routers import book_router
from genre.routers import genre_router
from settings import settings
from user.routers import auth_router, user_router

router = APIRouter(
    prefix=settings.PREFIX,
)

router.include_router(auth_router, prefix='/users', tags=['User'])
router.include_router(user_router, prefix='/users', tags=['User'])
router.include_router(book_router, prefix='/books', tags=['Book'])
router.include_router(genre_router, prefix='/genres', tags=['Genre'])
