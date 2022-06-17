from flask import escape
from app import socketio



def emit_friend_message_to_sid(user_tag, message, sid):
    message = escape(message)
    socketio.emit('friend_message', {'user_tag': user_tag, 'message': message}, room=sid)

def emit_friend_request_to_sid(sid, user_tag_of_sender):
    socketio.emit('friend_request', {'user_tag': user_tag_of_sender}, room=sid)
