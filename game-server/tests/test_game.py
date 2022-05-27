import unittest
import inspect
from flask import current_app
from app import create_app
from app.blueprints.game_two.models.game import Game
from app.blueprints.game_two.models.game_manager import GameManager

def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]

def prnt(val, label=''):
    '''
    Print wrapper for clear logging
    '''
    if not label:
        label = retrieve_name(val)
    print(f"\n{label}: {val}\n", flush=True)


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
        self.game = Game([1,2])

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_game_creation(self):
        assert type(self.game) == Game

    def test_id_in_game(self):
        game = Game(['1','2'])
        self.assertEqual(game.is_player_in_game(1), False)
        self.assertEqual(game.is_player_in_game('1'), True)
