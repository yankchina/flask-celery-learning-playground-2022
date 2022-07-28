from app import socketio


def emit_notification(notification, sid):
    if isinstance(sid, list):
        sid = [sid]
    for sid in sid:
        socketio.emit('notification', { 'notification': notification }, room=sid)

def emit_notification_json(notification, sid):
    if isinstance(sid, list):
        sid = [sid]
    for sid in sid:
        socketio.emit('notification_json', { 'notification_json': notification }, room=sid)
