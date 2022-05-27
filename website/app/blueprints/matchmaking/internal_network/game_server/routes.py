import time
from flask import request, jsonify, current_app
from app import cache
from app.blueprints.matchmaking import bp
from app.blueprints.matchmaking.sockets import emit_find_match_status, send_match_found_accept_request_to_users, send_user_ids_to_game
from slg_utilities.helpers import prnt

from app.blueprints.matchmaking.tasks import check_matchmaking_accept, find_match, update_queued_players_in_cache
from app.helpers.models import get_user_from_id
from app.blueprints.matchmaking.resets import clear_match_found, reset_all
from app.blueprints.matchmaking.internal_network.game_server.request import request_game_deletion
from app.blueprints.matchmaking.cache_helpers import get_key_from_id_map_cache



@bp.route('/game_created_successfully')
def game_created_successfully():
    '''
    Data passed to this route is:
        - key (str): secret key that was passed back and forth to authenticate
        - players (list<str>): list of player/user ids that we initially sent from our mongodb
        - server (str): server ip address and port (ie 127.0.0.1:5001)
        - game_id (str): game_id for users to connect to when they connect to the game server

    Example request from game-server:
    '''
    data = request.args.to_dict(flat=False)

    prnt(data)
    print(data, flush=True)

    if data.get('key')[0] != current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'):
        return jsonify({'success': False})

    if current_app.config.get("TESTING"):
        return jsonify({'success': True, 'message': f"TESTING: Calling send_user_ids_to_game(data.get('players'), data.get('server')[0], data.get('game_id')[0])"})

    # send accept / reject request to each connected user
    cache_key = send_match_found_accept_request_to_users(data.get('players')) # this needs to write player choices somewhere
    print(cache_key, flush=True)

    time.sleep(8)

    player_accept_statuses = cache.get(cache_key) or {}

    users_accepted = []
    users_declined = []

    for user_id, accepted in player_accept_statuses.items():
        if accepted:
            users_accepted.append(user_id)
        else:
            users_declined.append(user_id)

    if len(users_declined) > 0:
        # update the cache and put the accepted users at the front of the line
        users_accepted_info = list(map(lambda user_id: get_user_from_id(user_id).get_matchmaking_info(), users_accepted))
        update_queued_players_in_cache.apply_async((users_accepted_info, "front"))

        # remove declined users from the queue
        for user_id in users_declined:
            reset_all(user_id)

        # send update to accepted users to clear out their game_found html
        for user_id in users_accepted:
            clear_match_found(user_id)

        # send update to game server to kill the created game
        request_game_deletion(request.environ.get("REMOTE_ADDR"), 5001, data.get('game_id')[0])

        # emit a find_match for any one of the players
        task = find_match.apply_async(args=[], priority=0)
        sid = get_key_from_id_map_cache(user_id, 'sid')
        emit_find_match_status(sid, task.id)

        return jsonify({'success': True})
    else:
        send_user_ids_to_game(data.get('players'), f'http://{request.environ.get("REMOTE_ADDR")}:5001', data.get('game_id')[0])
        # assign_users_as_in_game(data.get('players'))
        #

    # check_matchmaking_accept.apply_async((8, cache_key,  f'http://{request.environ.get("REMOTE_ADDR")}:5001', data.get('game_id')[0]))
        # set up an async task to run in 8 seconds that checks player choices in the cache
        # ---> if all users accept:
            # if all are true then we call send_user_ids_to_game
        # ---> if any users decline:
            # move all users to front of the matchmaking player cache



    # if each user

    # if our secret key is verified then we send the user_ids to the game
    # send_user_ids_to_game(data.get('players'), f'http://{request.environ.get("REMOTE_ADDR")}:5001', data.get('game_id')[0])

    return jsonify({'success': True})
