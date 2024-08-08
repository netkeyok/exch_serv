import asyncio

from celery import Celery
from celery.schedules import crontab

from api_requests.send_to_cv import send_articles, clear_old_docs, clean_tables_list
from db_connections.db_conf import REDIS_HOST, REDIS_PASS
from api_requests.send_to_sm import send_wi

celery_app = Celery("tasks", broker=f"redis://:{REDIS_PASS}@{REDIS_HOST}:6379/0")
celery_app.conf.timezone = "Asia/Yekaterinburg"

celery_app.conf.beat_schedule = {
    "add-every-5-minutes": {
        "task": "tasks.tasks.start_send_docs",
        "schedule": crontab(minute="*/5", hour="8-23"),
    },
    "send-articles-daily-at-7am": {
        "task": "tasks.tasks.start_send_articles",
        "schedule": crontab(minute="0", hour="7"),
    },
    "clear-docs-daily-at-23pm": {
        "task": "tasks.tasks.task_clear_old_docs",
        "schedule": crontab(minute="0", hour="23"),
    },
    "clear-tables-weekly-at-23pm": {
        "task": "tasks.tasks.task_clear_old_doc_tables",
        "schedule": crontab(minute="0", hour="23"),
    },
}


@celery_app.task
def start_send_docs():
    result = asyncio.run(send_wi())
    return result


@celery_app.task
def start_send_articles():
    result = asyncio.run(send_articles())
    return result


@celery_app.task
def task_clear_old_docs():
    result = asyncio.run(clear_old_docs(7))
    return result


@celery_app.task
def task_clear_old_doc_tables():
    result = asyncio.run(clean_tables_list(7))
    return result
