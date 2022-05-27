from flask import render_template
from app.blueprints.game_two import bp
from app import socketio



@bp.route('/request_connection')
def request_connection():

    return render_template('index.html')


@socketio.on('connect')
def connect(data):
    pass

    # get the game id passed with the user