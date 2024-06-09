import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from base.logging import LogConfig
from user.routers import user_router

dictConfig(LogConfig().dict())
logger = logging.getLogger('app')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Started fastapi')

    yield

    logger.info('Stopped fastapi')


app = FastAPI(title='E-Books-Catalog', lifespan=lifespan)

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix='/users', tags=['User'])
app.include_router(main_api_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
