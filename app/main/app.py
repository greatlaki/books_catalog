import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI

from base.logging import LogConfig
from main.routers import router

dictConfig(LogConfig().dict())
logger = logging.getLogger('app')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Started fastapi')

    yield

    logger.info('Stopped fastapi')


app = FastAPI(title='E-Books-Catalog', lifespan=lifespan)

app.include_router(router)
