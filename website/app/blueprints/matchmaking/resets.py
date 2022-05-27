'''
    This module defines functions that reset users back to base states
'''
from app.blueprints.matchmaking.cache_helpers import get_key_from_id_map_cache

from app import socketio, cache
from app.helpers.models import get_user_from_id
from app.blueprints.matchmaking.sockets import emit_clear_match_found, emit_reset_all_matchmaking
from slg_utilities.helpers import prnt


def reset_all(user_id):
    user = get_user_from_id(user_id)
    user.datetime_joined_queue = None
    user.in_game_id = None
    user.save()
    sid = get_key_from_id_map_cache(user_id, 'sid')
    emit_reset_all_matchmaking(sid)

def clear_match_found(user_id):
    sid = get_key_from_id_map_cache(user_id, 'sid')
    emit_clear_match_found(sid)
