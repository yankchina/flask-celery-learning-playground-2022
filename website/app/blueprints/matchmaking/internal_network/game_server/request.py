from app import celery
from flask import current_app
import requests
import asyncio


def request_game_creation(server: str, port: any, player_ids: list):
    # super hacky way to make a request without getting response
    try:
        requests.get(f'http://{server}:{port}/create_game', params={'key': current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'), 'players': player_ids}, timeout=0.000000001)
    except requests.exceptions.ReadTimeout:
        pass

def request_game_deletion(server, port, game_id):
    try:
        requests.get(f'http://{server}:{port}/delete_game', params={'key': current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'), 'game_id': game_id}, timeout=0.000000001)
    except requests.exceptions.ReadTimeout:
        pass

@celery.task()
def request_game_creation_task(server: str, port: any, player_ids: list):
    requests.get(f'http://{server}:{port}/create_game', params={'key': current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'), 'players': player_ids})
