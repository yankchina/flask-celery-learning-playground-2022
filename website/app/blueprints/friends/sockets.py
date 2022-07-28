from flask import escape
from app import socketio
from slg_utilities.helpers import prnt



def emit_friend_message_to_sid(user_tag, message, sid):
    message = escape(message)
    socketio.emit('friend_message', {'user_tag': user_tag, 'message': message}, room=sid)

def emit_friend_request_to_sid(sid, user_tag_of_sender, user_id_of_sender):
    socketio.emit('friend_request', {'user_tag': user_tag_of_sender, 'user_id': user_id_of_sender}, room=sid)

def emit_party_invite_to_sid(user_tag, sid):
    prnt(sid)
    print(sid, flush=True)
    prnt(user_tag)
    if sid:
        socketio.emit('party_invite', {'user_tag': user_tag}, room=sid)
    # else we just dont emit it but we append it to the users party invitations

def emit_party_message_to_sid(message_dict, sid):
    socketio.emit('party_message', {'message_dict': message_dict}, room=sid)