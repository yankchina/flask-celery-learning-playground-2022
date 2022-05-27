from flask import Blueprint

bp = Blueprint(
    'sockets',
    __name__,
    template_folder="templates",
    static_folder="static"
)

from app.blueprints.sockets import routes