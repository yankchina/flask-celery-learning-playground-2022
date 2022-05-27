from flask import jsonify, current_app, request
from app.blueprints.game_two import bp
import time
from slg_utilities.helpers import print_object_attrs


@bp.route('/test_response')
def test_response():
    print(current_app.game_manager, flush=True)
    print(current_app.game_manager.games, flush=True)
    return jsonify({'success': True})


@bp.route('/test_get_request_from_website')
def test_get_request_from_website():
    time.sleep(2)
    print(request, flush=True)
    # print_object_attrs(request)
    return jsonify({'success': True})