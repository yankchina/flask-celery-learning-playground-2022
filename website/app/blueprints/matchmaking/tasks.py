from app import cache, celery, socketio
from flask_login import current_user
from flask import current_app
from app.blueprints.matchmaking.matchmaking import players_are_suitable_match, find_match_for_all_players, find_match_for_player
import time

from app.blueprints.matchmaking.sockets import send_user_ids_to_game


@celery.task(bind=True)
def find_match(self, user_info=None):
    players = cache.get('queued-players') or []

    if user_info:
        # strip added player from players if it exists
        players = [p for p in players if p['id'] != user_info['id']]
        players.append(user_info)
        cache.set('queued-players', players, timeout=0)

    match_players = find_match_for_all_players(players)
    if match_players:
        players = [p for p in players if p not in match_players]
        cache.set('queued-players', players, timeout=0)
        return match_players

    return None

@celery.task()
def update_queued_players_in_cache(players_to_add, where_to_add="front"):
    current_queue = cache.get('queued-players')
    if where_to_add == "front":
        new_queue = players_to_add + current_queue
    elif where_to_add == "back":
        new_queue = current_queue + players_to_add
    cache.set('queued-players', new_queue, timeout=0)



@celery.task()
def check_matchmaking_accept(delay_time, cache_key, server, game_id):
    time.sleep(delay_time)
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

        # and possibly send update to game server to kill the created game
        pass
    else:
        send_user_ids_to_game(users_accepted, server, game_id)








# @celery.task()
# def task_leave_matchmaking(user_id):
#     try:
#         players = cache.get('queued-players') or []
#         players = [p for p in players if p['id'] != user_id]
#         cache.set('queued-players', players)
#         print(players, flush=True)
#         # logger.debug('User successfully left matchmaking')
#         return True
#     except:
#         return False
#         # logger.exception('CELERY | Issue with task_leave_matchmaking as described by exception')
