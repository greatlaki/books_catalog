from asgiref.sync import async_to_sync
from celery import Celery
from celery.schedules import crontab

from book.services import cancel_reserve_background
from settings import settings

celery = Celery('tasks')
celery.conf.broker_url = settings.CELERY_BROKER_URL


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='00', minute='00'), schedule_cancel_reserve.s())


@celery.task
def schedule_cancel_reserve():
    async_to_sync(cancel_reserve_background)()
