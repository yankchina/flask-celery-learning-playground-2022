from flask import Blueprint

bp = Blueprint(
    'notifications',
    __name__,
    template_folder="templates",
    # url_prefix='/friends',
    static_folder='static'
)

# from app.blueprints.notifications import routes, context_processors