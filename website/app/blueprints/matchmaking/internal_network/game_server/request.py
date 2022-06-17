from app import celery
from flask import current_app, Response
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

def request_game_info(server, port):
    # resp = requests.get(f'http://{server}:{port}/query_games_running', params={'key': current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY')})
    # return resp.json
    r = requests.get(f'http://{server}:{port}/query_games_running', params={'key': current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY')})
    return Response(
        r.text,
        status=r.status_code,
        content_type=r.headers['content-type'],
    )

def request_game_info_from_all_servers(port=5001):
    game_servers = current_app.config.get('GAME_SERVERS')
    server_info = {}
    for server in game_servers:
        server_info[server] = request_game_info(server, port)
    return server_info

@celery.task()
def request_game_creation_task(server: str, port: any, player_ids: list):
    requests.get(f'http://{server}:{port}/create_game', params={'key': current_app.config.get('GAME_SERVER_AUTHENTICATION_KEY'), 'players': player_ids})
