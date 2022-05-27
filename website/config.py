import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    MONGODB_SETTINGS = {
        "db": "doodler-website",
        "host": "mongo"
        # "host": "mongodb://127.0.0.1:27017/doodler-website"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    POSTS_PER_PAGE = 25
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')
    HASHING_ALGORITHM = os.environ.get('HASHING_ALGORITHM' , 'HS256')
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD' , 'update_redis_password')

    GAME_SERVER_AUTHENTICATION_KEY = os.environ.get('GAME_SERVER_AUTHENTICATION_KEY', 'update-game-server-auth-key')

class ShellConfig(Config):
    MONGODB_SETTINGS = {
        "db": "doodler-website",
        "host": "127.0.0.1",
        'port': 27018
        # "host": "mongodb://127.0.0.1:27017/doodler-website"
    }