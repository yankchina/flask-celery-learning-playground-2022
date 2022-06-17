from flask import jsonify, current_app, request
from app.blueprints.game_two import bp


@bp.route('/query_games_running')
def query_games_running():
    print('query received', flush=True)
    for g in [str(game) for game in current_app.game_manager.games]:
        print(g, flush=True)
    return jsonify({'games_running': 0})