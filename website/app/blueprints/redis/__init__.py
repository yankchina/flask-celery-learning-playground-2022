from flask import Blueprint

bp = Blueprint('redis', __name__)

from app.blueprints.redis import routes