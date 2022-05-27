from abc import abstractmethod, ABC


'''
NOTES

Games need some concept of authorized actions.

Whether thats a list tied to each user in a state dictionary or what have you,
the authorized actions needs to authorize specific game actions a player can take
at a certain time.

Authorized actions need to be either emits or whatever


Perhaps we could do something like this:

self.authorization_mapping = {
    'name-of-authorization': self.method
}

and then assign names of authorizations to players

game: {
    playerId1 = {
        'score': 0,
        'authorizations': ['name-of-authorization', etc...]
    }
}


'''



class BaseGame(ABC):
    '''
        Parameters:

            players (list): Can be list of tuples, strings, etc...
                                HOWEVER:
                                    It needs to have some sort of ID's associated with each player.
                                    That association needs to be defined by the class instance's
                                    id_accessor attribute

            id_accessor (func): A lambda (or function) that takes in one argument:
                                    The player object as per defined when passing in the players
                                    So if we were to define players as a tuple of (id, mmr)
                                    We can define the id_accessor like:
                                        lambda player: player[0]

                                    This gives us flexibility in how we want to define each player
    '''

    #TODO; MAKE DECORATOR THAT VERIFY PLAYER IS IN GAME
    # def verify_is_in_game(self, func):
    #TODO; MAKE DECORATOR THAT VERIFY THE PLAYER REQUESTING AN ACTION IS THAT PLAYERS TURN
    # def verify_is_turn(self, func):

    def __init__(
        self,
        players: list,
        id_accessor=lambda player: player,
        current_round=1,
        num_rounds=3
    ):
        self.players = players
        self.player_ids = {id_accessor(player) for player in players}
        self.id_accessor = id_accessor
        self.current_round = current_round
        self.num_rounds = num_rounds

        self.initial_state = {
            'initial_round' : current_round,
        }

    def is_player_in_game(self, player_id: str) -> bool:
        if player_id in self.player_ids:
            return True
        return False

    @abstractmethod
    def round_loop(self):
        '''
        Defined in the child

        Example:

            self.game_action_one()
            self.game_action_two()

            if round_over:
                self.end_round()
        '''
        pass

    def start_round(self):
        self.increment
        self.round_loop()

    def end_round(self):

        self.current_round += 1
        if self.current_round > self.num_rounds:
            self.base_game_end()

    def base_game_end(self):
        self.current_round = self.initial_state['initial_round']
        self.clear_cache

    @abstractmethod
    def game_end_child(self):
        pass

    # decorator ; Dont know how to get this to work as of this moment
    # def verify_player_in_game(func):
    #     def outer(self):
    #         def inner(player_id, *args, **kwargs)
    #             print('verifying if player is in game', flush=True)
    #             if not self.is_player_in_game(player_id):
    #                 return False
    #             else:
    #                 return func(self, *args, **kwargs)
    #         return inner

    #     return outer

    def verify_player_in_game(self, player_id):
        '''
        If player is not in game then we return False, else True

        Use in a method like so: (Unfortunately I don't have time to figure out how to apply a decorator within the class, that uses instance variables)

            if not self.verify_player_in_game(player_id):
                return False

        Yes, unfortunately this involves two lines instead of one outer decorator line, but its the best we can do right now
        '''
        return self.is_player_in_game(player_id)

    def to_json(self):
        ignore_keys = ['id_accessor', 'players']
        json = {key: value for key, value in vars(self).items() if key not in ignore_keys}
        print(json)
        return json

    def __repr__(self):
        base_string = [f'\t{key}: {value}\n' for key, value in self.to_json().items()]
        return 'Game:\n' + ''.join(base_string)

    def __str__(self):
        base_string = [f'\t{key}: {value}\n' for key,
                       value in self.to_json().items()]
        # base_string = ''
        return 'Game:\n' + ''.join(base_string)