import os
import time

from app import celery


# celery = Celery(__name__)
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
# celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task()
def add_together(a, b):
    print('hello from celery', flush=True)
    return a + b