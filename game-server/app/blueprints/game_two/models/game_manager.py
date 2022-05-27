

from typing import Any, NewType


GameId = NewType('GameId', int)


class GameManager:

    def __init__(self, game_class):
        self.games = {}
        self.game_class = game_class

    def create_game(self, *game_args, **game_kwargs):
        ''' Returns game_id '''
        new_id = self.get_id()
        self.games[new_id] = self.game_class(*game_args, **game_kwargs)
        return GameId(new_id)

    def destroy_game(self, id_):
        del self.games[id_]

    def get_id(self):
        len_ = len(self.games)
        for i in range(len_):
            if i not in self.games:
                return i
        return len_

    def num_games_running(self):
        return len(self.games)

    def get_games_running(self):
        return self.games

    def get_game_id_from_player_id(self, player_id: Any):
        for game_id, game in self.games.items():
            if game.is_player_in_game(player_id):
                return game_id

    def get_game_by_id(self, id_):
        return self.games[int(id_)]