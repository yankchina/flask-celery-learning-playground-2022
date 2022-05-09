from flask import current_app


def players_are_suitable_match(player1, player2):
    # TODO
    return True

def find_match_for_all_players(player_pool):
    print("finding match for all players")
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
    # parse requirements for player and then match
    for p in player_pool:
        if players_are_suitable_match(player, p):
            game_players.append(p)
            if len(game_players) >= num_players:
                return game_players
    return False