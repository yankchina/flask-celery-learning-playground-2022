import requests
from flask import jsonify
from app.blueprints.matchmaking import bp
from app import cache
from slg_utilities.helpers import prnt


@bp.route('/test_request_to_game_server')
def test_request_to_game_server():
    resp = requests.get('http://game-server-1:5001/test_get_request_from_website')
    print(f'Got data: {resp.json()}', flush=True)
    return jsonify({'message': 'sent request'})

@bp.route('/check_redis_queue')
def test_check_redis_queue():
    queue = cache.get('queued-players')
    prnt(queue)
    return jsonify({'queue': queue})