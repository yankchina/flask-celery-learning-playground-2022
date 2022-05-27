from flask import render_template, jsonify
from flask_login import current_user
from app.blueprints.main import bp
from app.blueprints.matchmaking.tasks import find_match
from app.blueprints.main.tasks import add_together

def get_game_server():
    print('getting game server', flush=True)
    return '127.0.0.1:5001'

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/join_game')
def join_game():
    pass