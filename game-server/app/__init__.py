import os
from flask import Flask
from config import Config
from flask_socketio import SocketIO
from logger_slg import init_logger
from flask_cors import CORS


socketio = SocketIO(
    async_mode="gevent", ping_timeout=30, ping_interval=10,
    manage_session=False,
    logger=True, # engineio_logger=True,
    cors_allowed_origins=[
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ]
)
cors = CORS(
    resources={r"*": {"origins": [
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ]}}
)

def create_app(config_class=Config):
    # putting these imports here because of circular dependency
    from app.blueprints.game_two.models.game_manager import GameManager
    from app.blueprints.game_two.models.game import Game

    app = Flask(__name__)
    app.config.from_object(config_class)

    app.logger = init_logger(
        log_path=f"{os.path.abspath(os.path.dirname(__file__))}/log.log"
    )

    app.game_manager = GameManager(Game)

    cors.init_app(app)

    from app.blueprints.game_two import bp as bp_game
    app.register_blueprint(bp_game)

    socketio.init_app(app)

    return app
