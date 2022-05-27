from flask import jsonify, current_app, request
from app.blueprints.game_two import bp
import requests
from slg_utilities.helpers import print_object_attrs, prnt

@bp.route('/create_game')
def create_game():
    '''
    Expects request that looks like this:

        requests.get(f'http://{server}:{port}/create_game', params={'key': current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'), 'players': player_ids}, timeout=0.000000001)

    '''
    data = request.args.to_dict(flat=False)
    player_ids = data.get('players')


    if data.get('key')[0] != current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'):
        current_app.logger.exception(f"Error: \n\tKey supplied: {data.get('key')[0]}\n\tServer key: {current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY')}")
        return jsonify({'success': False})
    try:
        game_id = current_app.game_manager.create_game(players=player_ids)
    except:
        joined_ids = '\n\t\t'.join(player_ids)
        current_app.logger.exception(f"Failed to create game.\n\tPlayer ID's:\n\t\t{joined_ids}")
        return jsonify({'success': False})

    request_data = {
        'key': data.get('key')[0],
        'players': player_ids,
        'game_id': game_id
    }
    requests.get(f'http://website:5000/game_created_successfully', params=request_data)

    return jsonify({'success': True, 'request_data': request_data})
