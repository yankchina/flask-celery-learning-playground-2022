from flask import Blueprint

bp = Blueprint(
    'friends',
    __name__,
    template_folder="templates",
    url_prefix='/friends',
    static_folder='static'
)

from app.blueprints.friends import routes, context_processors