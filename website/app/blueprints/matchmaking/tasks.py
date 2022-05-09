from app import cache, celery
from flask_login import current_user
from flask import current_app
# from app import celery
from app.blueprints.matchmaking.matchmaking import players_are_suitable_match, find_match_for_all_players, find_match_for_player
from app.helpers.helpers import throttle_print
import time

# heres where we can define our celery tasks



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

    # return 'getting this return value from celery'






# @app.route('/add_user', methods=['POST'])

#     # add to player pool immediately
#     players.add(user)

#     # run request for matchmaking which tries to find a game for the first person in the queue first FIFO
#     request_matchmaking(user_id)

#     #  (NON URGENT) - if a match is found, update estimated wait time for other users in queue
#     #  (NON URGENT) - log number of attempts to find a game for a user. if they cant find a game, loosen the requirements for matching them with other players

#     # figure out how to use celery for this task
#     # add job to celery queue, how do we update celery queue with appropriate players each time
#     PLAYER_POOL.append(request.form.get('player_id'))
#     print(PLAYER_POOL, flush=True)
#     # players = find_match(PLAYER_POOL)
#     # return jsonify({'players': players})


# @celery.task(name="request_matchmaking")
# def request_matchmaking(player_id):
#     # get players from the cache
#     players = cache.get('players') or []

#     # when this actually goes through, we need to first make sure if the player who requested is still in the player pool
#     if player_id not in players:
#         return 'Player is in game or left matchmaking'