import uuid
from flask_login import current_user
from flask import render_template, request, url_for
from app import socketio, cache
from app.blueprints.matchmaking.cache_helpers import update_cache_object, get_key_from_id_map_cache
from app.helpers.models import get_user_from_id
from app.blueprints.matchmaking.matchmaking import accept_match, check_if_match_is_ready, decline_match

@socketio.on('connect')
def connect():
    update_cache_object('id_map', str(current_user.id), data={'username': current_user.username, 'sid': request.sid}, timeout=1200)

def emit_join_game(sid, server, game_id):
    socketio.emit('join_game', { 'server': server, 'game_id': game_id, 'html': render_template('game.html') }, room=sid)

def send_user_ids_to_game(user_ids: list, server, game_id: str):
    for id_ in user_ids:
        user = get_user_from_id(id_)
        user.leave_queue()
        sid = get_key_from_id_map_cache(id_, 'sid')
        emit_join_game(sid, server, game_id)

def emit_match_found_accept_request_to_user(sid, cache_key):
    socketio.emit('match_found', { 'key': cache_key }, room=sid)

def send_match_found_accept_request_to_users(user_ids: list):
    # generate a cache_key that the user sends their result to
    cache_key = str(uuid.uuid4())
    cache.set(cache_key, {user: False for user in user_ids})
    for id_ in user_ids:
        user = get_user_from_id(id_)
        # optimization opportunity; can pull the id_map and then iterate over it once
        sid = get_key_from_id_map_cache(id_, 'sid')
        emit_match_found_accept_request_to_user(sid, cache_key)
    return cache_key

@socketio.on('match_found_choice')
def match_found_choice(data):
    print(current_user, flush=True)
    print(current_user.id, flush=True)
    key = data.get('key')
    print(key, flush=True)
    if not key:
        return
    if data.get('choice') == "accept":
        accpt_success = accept_match(key, str(current_user.id))
    else:
        decline_match(str(current_user.id))

    # if accpt_success:
    #     match_ready_ids = check_if_match_is_ready(key)
    #     if match_ready_ids: # match_ready is actually the user_ids
    #         send_user_ids_to_game(match_ready_ids)
    #         cache.delete(key)

        # check to see if all values are True
    # request.sid

def emit_reset_all_matchmaking(sid):
    socketio.emit('reset_all_matchmaking', room=sid)

def emit_clear_match_found(sid):
    socketio.emit('clear_match_found', room=sid)

def emit_find_match_status(sid, task_id):
    socketio.emit(
        'ping_find_match',
        { 'location': url_for('matchmaking.find_match_task_status', task_id=task_id) },
        room=sid
    )