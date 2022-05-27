import time
import unittest
import inspect
from flask import current_app
from app import create_app
from slg_utilities.helpers import prnt, print_object_attrs, print_items
from config import Config

class TestConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {
        # "db": "doodler-backend-testing",
        "host": "mongodb://127.0.0.1:27017/doodler-backend-testing"
        # "host": "mongodb://127.0.0.1:27017/doodler-website"
    }
    GAME_SERVER_AUTHENTICATION_KEY = "my-test-secret-key"

class TestLoadDataFunctions(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls.shared_resource = random.randint(1, 100)

    # @classmethod
    # def tearDownClass(cls):
    #     cls.shared_resource = None

    def setUp(self):
        self.app = create_app(TestConfig)
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client1 = self.app.test_client()
        self.client2 = self.app.test_client()
        prnt(self.client1)
        prnt(self.client2)

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_two_clients_join_matchmaking(self):
        resp = self.client1.get('/join_matchmaking')
        self.assertEqual(True, resp.json['success'])
        self.assertIn('location', resp.json)
        resp = self.client2.get('/join_matchmaking')
        self.assertEqual(True, resp.json['success'])
        self.assertIn('location', resp.json)

        # not sure how to ping task status location and subsequently return users to game
        # # resp.
        # task_location = resp.json['location']
        # task_status_response = self.client2.get(task_location)
        # print(task_status_response, flush=True)
        # server emits to users a queue accept request
        # users select Accept or Decline
        # if all Accept:
        #   server sends emit with game server and game id for players to join
        # if any Decline:
        #   Users that declined have everything (regarding matchmaking) reset for themselves and are removed from queue
        #   Users that accepted are placed at the front of the redis cache of players that are in the queue


    def test_both_clients_accept_queue(self):
        pass

    def test_only_one_client_accepts_queue(self):
        # of two
        pass

    def test_clear_matchmaking_frontend_indicators_on_unsuccessful_game_join(self):
        # Users that accepted only close queue pop, but remain in queue, and are placed at the front of the players cache
        pass

    def test_game_created_error_with_incorrect_key(self):
        resp = self.client1.get('/game_created_successfully', query_string={'players': ['1','2'], 'key': 'secret-key-for-game-creation'})
        self.assertEqual(resp.json['success'], False)

    def test_game_created_successfully_created(self):
        resp = self.client1.get('/game_created_successfully', query_string={'players': ['1','2'], 'key': 'my-test-secret-key'})
        self.assertEqual(resp.json['success'], True)
