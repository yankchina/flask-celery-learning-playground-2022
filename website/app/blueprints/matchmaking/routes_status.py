from app.blueprints.matchmaking.tasks import find_match
from app import socketio, cache
from flask import jsonify, render_template, current_app

from app.blueprints.matchmaking import bp
from app.blueprints.matchmaking.cache_helpers import get_key_from_id_map_cache
from app.blueprints.matchmaking.sockets import emit_join_game
from app.helpers.models import get_user_from_id
from app.blueprints.matchmaking.internal_network.game_server.request import request_game_creation, request_game_creation_task

@bp.route('/status/<task_id>')
def find_match_task_status(task_id):
    task = find_match.AsyncResult(task_id)

    if task.info:
        match_players = task.info
        player_ids = map(lambda p: p.get('id'), match_players)
        print('requesting game creation', flush=True)
        # request_game_creation('game-server-1', '5001', player_ids)
        request_game_creation('game-server-1', '5001', player_ids)
        return jsonify({'success': True, 'task_status': task.state})

        # send each player to the game
        # for p in match_players:

        #     # unset datetime_joined_queue for each user
        #     user = get_user_from_id(p.get('id'))
        #     user.leave_queue()

        #     sid = get_key_from_id_map_cache(p.get('id'), 'sid')
        #     emit_join_game(sid, '127.0.0.1:5001', 1)

    # print(dir(task), flush=True)
    return jsonify({'success': True, 'task_status': task.state})