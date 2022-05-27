import unittest
import inspect
from flask import current_app
from app import create_app
from app.blueprints.game_two.models.game import Game
from app.blueprints.game_two.models.game_manager import GameManager
from slg_utilities.helpers import prnt, print_object_attrs


class TestLoadDataFunctions(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls.shared_resource = random.randint(1, 100)

    # @classmethod
    # def tearDownClass(cls):
    #     cls.shared_resource = None

    def setUp(self):
        self.app = create_app()
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.game_manager = GameManager(Game)
        self.client = self.app.test_client()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_create_game_from_game_manager(self):
        self.game_manager.create_game([1,2])

    def test_number_of_games(self):
        self.game_manager.create_game([1,2])
        self.game_manager.create_game(['1','2'])
        self.game_manager.create_game(['string','hey','player2','player3'])
        self.assertEqual(self.game_manager.num_games_running(), 3)

    def test_player_id_access(self):
        self.game_manager.create_game([1,2])
        self.game_manager.create_game([('1', 1000),('2', 1200)], id_accessor=lambda player: player[0])
        self.game_manager.create_game([{'id': '1', 'mmr': 1000},{'id': '2', 'mmr': 1200}], id_accessor=lambda player: player['id'])
        self.game_manager.create_game(['string','hey','player2','player3'])
        self.assertListEqual(self.game_manager.games[1].players, [('1', 1000),('2', 1200)])
        self.assertSetEqual(self.game_manager.games[1].player_ids, {'1','2'})
        self.assertListEqual(self.game_manager.games[2].players, [{'id': '1', 'mmr': 1000},{'id': '2', 'mmr': 1200}])
        self.assertSetEqual(self.game_manager.games[2].player_ids, {'1','2'})
        self.assertListEqual(self.game_manager.games[3].players, ['string','hey','player2','player3'])
        self.assertSetEqual(self.game_manager.games[3].player_ids, {'string','hey','player2','player3'})

    def test_id_in_game(self):
        self.game_manager.create_game(['1','2'])
        self.assertEqual(self.game_manager.games[0].is_player_in_game(1), False)
        self.assertEqual(self.game_manager.games[0].is_player_in_game('1'), True)

    def test_get_game_id_from_player_id(self):
        self.game_manager.create_game([1,2])
        self.game_manager.create_game(['1','2'])
        self.assertEqual(self.game_manager.get_game_id_from_player_id('2'), 1)
        self.assertEqual(self.game_manager.get_game_id_from_player_id(2), 0)

    def test_create_game_request(self):
        self.client.get('/create_game', query_string={'players':['1','2']})
        self.assertSetEqual(self.app.game_manager.games[0].player_ids, {'1', '2'})

        # query strings are converted to strings so the original type cannot be determined; thus the player ids are strings
        resp = self.client.get('/create_game', query_string={'players': [1,2]})
        self.assertSetEqual(self.app.game_manager.games[1].player_ids, {'1','2'})

        value = getattr(resp, 'json')
        # prnt(resp.json)
        # prnt(resp.get_json())

        # print_object_attrs(resp, try_call_functions=False)