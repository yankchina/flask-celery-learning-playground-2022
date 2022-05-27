from flask import jsonify, current_app, request
from app.blueprints.game_two import bp


@bp.route('/query_games_running')
def query_games_running():
    return jsonify({'games_running': current_app.game_manager.games})