from flask import Flask, render_template, request, jsonify
from app import socketio



MAX_PLAYERS = 2

GAMES_RUNNING = {
    # id: {Game instance}
}

# this stores the players socket id to the game id they are currently in; for near instantaneous lookups of game state from verified users
PLAYER_GAME_MAP = {
    # socket_id: game_id
}


def assign_player_to_game(game_id, socket_id):
    PLAYER_GAME_MAP[socket_id] = game_id



@socketio.on('connect')
def connect(data):
    # matchmaking creates a very complex unique ID that is passed along and that is the game ID on connect
    # we assign the player to the game and the game to the player in the respective mappings for instantaneous lookup of players
    print(request.args.get('game_id'), flush=True)

    game_id = request.args.get('game_id')
    socket_id = request.args.get('socket_id')

    if game_id not in GAMES_RUNNING:
        return jsonify({'type': 'error', 'message': 'Game does not exist'})

    # check for if the player is assigned to this game from the website
    if not GAMES_RUNNING[game_id].player_in_game(socket_id):
        return jsonify({'type': 'error', 'message': 'Player is not in this game'})

    assign_player_to_game(game_id, socket_id)

    return jsonify({'type': 'success', 'message': 'Player successfully added to game!'})


@socketio.on('disconnect')
def handle_disconnect():
    return

def get_game_from_socket_id(socket_id):
    return GAMES_RUNNING.get(PLAYER_GAME_MAP.get(socket_id, ''))

@socketio.on('add_to_score')
def add_to_score(data):
    socket_id = request.sid
    print(data, flush=True)

    game = get_game_from_socket_id(socket_id)
    if not game:
        return jsonify({'type': 'error', 'message': 'Player not found in game'})

    game.increase_score(socket_id, data.get('answer', ''))
