from app import cache


def players_are_suitable_match(player1, player2):
    # TODO
    return True

def find_match_for_all_players(player_pool):
    for i in range(len(player_pool) - 1):
        try:
            game_players = find_match_for_player(player_pool[i], player_pool[:i] + player_pool[i+1:])
            if game_players:
                return game_players
        except:
            pass
            # current_app.logger.exception('Unknown exception')
    return False

def find_match_for_player(player, player_pool, num_players=2):
    # num_players is how many to find before returning a successful match

    game_players = [player]
    for p in player_pool:
        if players_are_suitable_match(player, p):
            game_players.append(p)
            if len(game_players) >= num_players:
                return game_players
    return False

def accept_match(cache_key, user_id):
    '''  '''
    current_status = cache.get(cache_key)
    if not current_status:
        return False
    current_status[user_id] = True
    cache.set(cache_key, current_status)
    return True

def decline_match(user_id):
    ''' Just pass for now and let the celery task handle the timeout '''
    pass

def check_if_match_is_ready(match_found_cache_key):
    ''' <match_found_cache_key> is an object of form {user_id: accept_bool, etc...} '''
    player_accept_status = cache.get(match_found_cache_key) or {}
    for accept_status in player_accept_status.values():
        if not accept_status:
            return False

    # return the player_ids so we can send them
    return list(player_accept_status.keys())