import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI

from base.logging import LogConfig
from main.routers import router
from pg.fixture import DatabaseFixtures

dictConfig(LogConfig().dict())
logger = logging.getLogger('app')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Started fastapi')
    await DatabaseFixtures().run()
    yield

    logger.info('Stopped fastapi')


app = FastAPI(title='E-Books-Catalog', lifespan=lifespan)

app.include_router(router)
