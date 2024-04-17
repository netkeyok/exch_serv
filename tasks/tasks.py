import asyncio

from celery import Celery
from celery.schedules import crontab

from api_requests.Send_to_CV import send_articles, clear_postuplenie
from db_connections.db_conf import REDIS_HOST, REDIS_PASS
from api_requests.Send_to_SM import send_wi

celery_app = Celery('tasks', broker=f'redis://:{REDIS_PASS}@{REDIS_HOST}:6379/0')
celery_app.conf.timezone = 'Asia/Yekaterinburg'

celery_app.conf.beat_schedule = {
    # 'add-every-5-minutes': {
    #     'task': 'tasks.tasks.start_send_docs',
    #     'schedule': crontab(minute='*/5', hour='8-23'),
    # },
    'send-articles-daily-at-7am': {
        'task': 'tasks.tasks.start_send_articles',
        'schedule': crontab(minute='0', hour='7'),
    },
    'clear-clear-docs-daily-at-6am': {
        'task': 'tasks.tasks.start_clear_docs',
        'schedule': crontab(minute='0', hour='6'),
    },
}


@celery_app.task
def start_send_docs():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(send_wi())
    return result


@celery_app.task
def start_send_articles():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(send_articles())
    return result


@celery_app.task
def start_clear_docs():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(clear_postuplenie())
    return result
