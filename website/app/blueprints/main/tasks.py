from app import celery

@celery.task()
def add_together(a, b):
    print('hello from celery', flush=True)
    return a + b