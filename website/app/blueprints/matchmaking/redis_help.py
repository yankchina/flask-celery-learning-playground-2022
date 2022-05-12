

# all these functions should just happen in a task so as to prevent
# any possibility of cache players array value conflict


# players are given an initial matchmaking state upon successfully joining queue
# this state is updated in the cache whenever the player makes an action and we can verify they are in a certain stage of the process
INITIAL_MATCHMAKING_STATE = lambda socket_id: {
    'notified_of_poll': '',
    'socket_id': socket_id,

}


def get_players_in_queue():
    pass
    # return players currently in the cache at this very moment

def add_player_to_queue():
    pass
    # add a player to the end of the existing redis cached players
