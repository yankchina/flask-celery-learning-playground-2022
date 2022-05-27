from flask import Blueprint

bp = Blueprint(
    'matchmaking',
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/static/matchmaking'
)

from app.blueprints.matchmaking import routes, routes_status
from app.blueprints.matchmaking.internal_network.game_server import routes

from app.blueprints.matchmaking.testing import routes
