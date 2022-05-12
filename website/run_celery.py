from app import celery, create_app
from init_celery import init_celery
from config import Config
app = create_app(Config)
init_celery(app, celery)