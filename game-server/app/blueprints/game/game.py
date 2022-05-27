import asyncio

class BaseGame:

    def __init__(
        self,
        players,
        num_rounds=3,
    ):
        pass


class Game:
    INITIAL_PLAYER_STATE = lambda name: {
        'name': name,
        'score': 0,
    }

    def __init__(self, id_="", start=0, round_count=3, players=[]):
        print('Game created', flush=True)
        self.id_ = id_
        self.counter = start
        self.game_running = False
        self.round_time = 10
        self.current_round = 0
        self.round_count = round_count
        self.current_player = 0
        self.initial_players = players

        self.player_states = {}

    def initialize_player_state(self, socket_id):
        # need to handle for IDs or something or some sort of identifier that is unique to the player; maybe their unique mongo database ID?
        self.player_states[socket_id] = self.INITIAL_PLAYER_STATE()

    def get_new_player_id(self):
        # return first number available from 1 - MAX_PLAYERS
        return

    def start_game(self):
        self.game_running = True

    def start_round(self):
        self.current_round += 1
        self.round_running = True
        self.start_round_timer()

    def end_round(self):
        self.round_running = False

    def handle_game_end(self):
        # redirect back home

        # send game information back to main server as POST request with the game ID and a generated password
        # so we can save the outcome of the game and handle any logic related to MMR, leaderboards,
        # player points, etc...
        pass

    async def start_round_timer(self):
        await asyncio.sleep(self.round_time)
        self.end_round()
        return 'Round over'

    def game_loop(self):
        while True:
            self.start_round()
            if self.current_round > self.round_count:
                self.handle_game_end()
                break

    def increment_counter(self):
        self.counter += 1

    def decrement_counter(self):
        self.counter -= 1

    def add_to_player_score(self, player_id, addition):
        self.players[player_id]['score'] += addition

    def subtract_from_player_score(self, player_id, subtraction):
        self.players[player_id]['score'] += subtraction