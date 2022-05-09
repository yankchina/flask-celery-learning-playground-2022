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
    print(current_user._get_current_object())
    print(current_user)
    # result = add_together.apply_async((2,3), countdown=2.0)
    # print(result, flush=True)

    return render_template('index.html')

@bp.route('/join_game')
def join_game():
    pass
    # find_match()
    # return jsonify({'server': get_game_server(), 'game_id': 1, 'html': render_template('game.html')}) # obfuscate later