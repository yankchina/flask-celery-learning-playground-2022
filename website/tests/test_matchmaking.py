
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
        self.client = self.app.test_client()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_game_created_error_with_incorrect_key(self):
        resp = self.client.get('/game_created_successfully', query_string={'players': ['1','2'], 'key': 'secret-key-for-game-creation'})
        prnt(resp.json)
        self.assertEqual(resp.json['success'], False)

    def test_game_created_successfully_created(self):
        resp = self.client.get('/game_created_successfully', query_string={'players': ['1','2'], 'key': 'my-test-secret-key'})
        prnt(resp.json)
        self.assertEqual(resp.json['success'], True)
