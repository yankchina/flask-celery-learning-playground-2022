from flask import Blueprint

bp = Blueprint('polling', __name__)

from app.blueprints.polling import routes, functions