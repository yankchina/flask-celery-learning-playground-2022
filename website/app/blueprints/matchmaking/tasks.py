from app import cache, celery
from flask_login import current_user
from flask import current_app
from app.blueprints.matchmaking.matchmaking import players_are_suitable_match, find_match_for_all_players, find_match_for_player
from app.helpers.helpers import throttle_print
import time

@celery.task(bind=True)
def find_match(self, user_info):

    players = cache.get('players') or []
    players.append(user_info)

    print('sleeping', flush=True)
    time.sleep(5)
    match_players = find_match_for_all_players(players)
    if match_players:
        # send each of the selected players to a game server
        players = [p for p in players if p not in match_players]
        cache.set('players', players)
        return match_players

    cache.set('players', players)

    return None
