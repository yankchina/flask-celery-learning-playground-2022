from flask import Blueprint

bp = Blueprint(
    'game-two',
    __name__,
    template_folder="templates",
    static_folder="static"
)

from app.blueprints.game_two.routes import connection, game_creation, test, game_deletion