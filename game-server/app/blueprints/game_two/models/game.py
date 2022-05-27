from app.blueprints.game_two.models.base_game import BaseGame
from flask import current_app




class Game(BaseGame):

    INITIAL_PLAYER_STATE = {
        'score': 0
    }

    def __init__(
        self,
        players: list,
        *args,
        **kwargs
    ):
        super().__init__(players, *args, **kwargs)
        # player list is defined in basegame
        # player accessor helpers are defined in basegame
        self.game_state = {self.id_accessor(player): self.INITIAL_PLAYER_STATE for player in players}

        # self.game_state = self.INITIAL_GAME_STATE(players)

    def add_to_score(self, player_id, score=2):
        if not self.verify_player_in_game(player_id):
            return False
        if not self.verify_is_players_turn(player_id):
            return False

        self.game_state['scores'][player_id] += score

    # def decrement_from_score(self, player_id, score=1):
    #     if not self.verify_player_in_game(player_id):
    #         return False
    #     self.game_state['scores'][player_id] -= score

    def get_game_state(self):

        return self.game_state

    def game_end_child(self):
        print('game end')

    def round_loop(self):

        def round_end_condition(self):
            pass

        pass
        # while True:

        # print('round_loop')

    def verify_is_players_turn(self, player_id):
        '''
        Similar to verify_player_in_game but this checks if its the players turn to make calls
        '''
        return self.current_turns_player_id == player_id