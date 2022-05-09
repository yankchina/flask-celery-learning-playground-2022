from flask import Blueprint

bp = Blueprint('matchmaking', __name__)

from app.blueprints.matchmaking import routes