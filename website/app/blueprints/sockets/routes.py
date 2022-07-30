from flask_login import login_required, current_user
from flask_socketio import join_room, leave_room, send
from flask import jsonify, url_for, render_template, request, current_app
from app import socketio
from app.blueprints.sockets import bp


# make so only admins can hit this route,
@bp.route('/emit_notification', methods=["POST"])
def emit_notification(data):
    socketio.emit('notification', { 'message': data.get('message') }, room=data.get('sid'))
    # socket_ids

@socketio.on('join_party_room')
def join_party_room(data):
    room = data['room']
    join_room(room)
    send('Joined room.', to=room)

@socketio.on('leave_party_room')
def leave_party_room(data):
    room = data['room']
    leave_room(room)
    send('Left room.', to=room)