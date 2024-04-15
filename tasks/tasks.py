import asyncio

from celery import Celery
from celery.schedules import crontab

from db_connections.db_conf import REDIS_HOST, REDIS_PASS
from api_requests.Send_to_SM import send_wi


celery_app = Celery('tasks', broker=f'redis://:{REDIS_PASS}@{REDIS_HOST}:6379/0')
celery_app.conf.timezone = 'Asia/Yekaterinburg'

celery_app.conf.beat_schedule = {
    'add-every-5-minutes': {
        'task': 'tasks.tasks.start_check_docs',
        'schedule': crontab(minute='*/5'),
    },
}


@celery_app.task
def start_check_docs():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(send_wi())
    return result
