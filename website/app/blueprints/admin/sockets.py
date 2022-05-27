from app import socketio

def emit_admin_notification(sid, message):
    socketio.emit('admin_notification', {'message': message}, room=sid)