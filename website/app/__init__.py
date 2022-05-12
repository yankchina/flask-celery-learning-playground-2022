from asyncore import poll
import os
import datetime
from flask import Flask, render_template, request, jsonify
from flask_login import current_user, LoginManager, login_user
from random import randint
from flask_caching import Cache
from flask_mongoengine import MongoEngine
from app.models.user import User
from app.models.unregistered_user import UnregisteredUser
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from flask_assets import Environment, Bundle
from celery import Celery
from init_celery import init_celery

import time

import random

login_manager = LoginManager()
login_manager.login_view = "home"

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
db = MongoEngine()
celery = Celery(
    __name__,
    broker=Config.CELERY_BROKER_URL,
    include=[
        "app.blueprints.main.tasks",
        "app.blueprints.matchmaking.tasks",
    ]
)
cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'website',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://redis:6379'
})


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    init_celery(app, celery=celery)

    app.task_list = []

    assets = Environment(app)
    assets.load_path = [
        os.path.join(os.path.dirname(__file__), 'static'),
    ]
    js_bundle = Bundle(
        'js/**/*.js',
        filters='jsmin',
        output='dist/app.js')
    assets.register('app-js', js_bundle)
    js_bundle.build(force=True)

    @login_manager.user_loader
    def load_user(user_id):
        for model in [User, UnregisteredUser]:
            try:
                user = model.objects(id=user_id).first()
                if user:
                    return user
            except Exception as e:
                pass

    @celery.task(name="create_task")
    def create_task():
        print(current_user)
        for i in range(3):
            print(i, flush=True)
            time.sleep(1)
        random_selection = [
            ['2owioejfiow', 'oaiwjefoijwe', 'oijwe'],
            ['oiaghhgu', 'iawjgigwiojwgieoj', 'mzxvnvc'],
            ['aowghweoi', 'woeirqq', 'pooiweu']
        ][random.randint(0,2)]
        return random_selection

    @app.route('/test_task')
    def start_long_running_task():
        output = create_task.delay()

        # for i in range(3):
        #     print(i, flush=True)
        #     time.sleep(1)
        print(output, flush=True)
        print('task completed', flush=True)
        return jsonify({'success': True})

    @app.route('/test_response')
    def test_response():
        return jsonify({'success': True})

    @app.before_request
    def auto_login_user():
        if not current_user.is_authenticated:
            user = UnregisteredUser()
            user.save()
            login_user(user, remember=True, duration=datetime.timedelta(days=30))

    @app.context_processor
    def seconds_since_joined_queue():
        if current_user.is_anonymous:
            return dict(seconds_since_joined_queue=None)
        return dict(seconds_since_joined_queue=current_user.get_seconds_since_joined_queue())

    from app.blueprints.main import bp as bp_main
    app.register_blueprint(bp_main)

    from app.blueprints.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    from app.blueprints.matchmaking import bp as bp_matchmaking
    app.register_blueprint(bp_matchmaking)

    from app.blueprints.polling import bp as bp_polling
    app.register_blueprint(bp_polling)

    # bp_polling.functions.async_get_data()

    return app
