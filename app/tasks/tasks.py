import asyncio
from celery import Celery
from celery.schedules import crontab

from book.services import cancel_reserve_background
from settings import settings

celery = Celery('tasks')
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery.conf.beat_schedule = {
    'run_cancel_reserve': {
        'task': 'cancel_reserve_background_task',
        'schedule': crontab(hour='00', minute='00'),
    }
}


@celery.task()
def cancel_reserve_background_task():
    loop = asyncio.get_running_loop()
    loop.run_until_complete(cancel_reserve_background)
