from fastapi import APIRouter

from settings import settings

router = APIRouter(
    prefix=settings.PREFIX,
)
