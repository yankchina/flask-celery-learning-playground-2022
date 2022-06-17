from flask import request, jsonify, current_app, render_template
from flask_login import current_user
from app.blueprints.friends import bp
from app.helpers.models import get_user_from_id, get_user_from_tag
from app.blueprints.friends.cache_helpers import get_sid_from_user_id
from app.blueprints.friends.sockets import emit_friend_request_to_sid
from slg_utilities.helpers import prnt



@bp.route('/friend_test', methods=["GET"])
def friend_test():
    return render_template('friends/index.html')

@bp.route('/send_friend_request', methods=["POST"])
def send_friend_request():
    prnt(request.form)
    user_tag = request.form.get('user_tag').strip()
    if not user_tag:
        return jsonify({'success': False, 'message': 'No user tag was passed.'})
    user = get_user_from_tag(user_tag)
    if not user:
        return jsonify({'success': False, 'message': 'Could not find user with that tag'})

    prnt(user)
    user.add_to_friend_requests(str(current_user.id))
    sid = get_sid_from_user_id(str(user.id))
    prnt(sid)
    emit_friend_request_to_sid(sid, current_user.user_tag)
    return jsonify({'success': True, 'message': f'Sent friend request to user'})

@bp.route('/add_friend', methods=["POST"])
def add_friend():
    prnt(request.form)
    user_id = request.form.get('user_id')
    if user_id not in current_user.friend_requests:
        return jsonify({'success': False, 'message': 'No authorization to do that'})
    try:
        user = get_user_from_id(user_id)
        user.add_friend(str(current_user.id)) # add_friend handles save
        current_user.add_friend(user_id)
        return jsonify({'success': True, 'message': f'{user.username} successfully added to friends list!'})
    except:
        current_app.logger.exception('Unknown error adding friend.')
        return jsonify({'success': False, 'message': 'Unknown error adding friend.'})

@bp.route('/remove_friend', methods=["POST"])
def remove_friend():
    user_id = request.form.get('user_id')
    try:
        current_user.remove_friend(user_id)
        return jsonify({'success': True, 'message': f'{user_id} successfully removed from friends list.'})
    except:
        current_app.logger.exception('Unknown error adding friend.')
        return jsonify({'success': False, 'message': 'Unknown error removing friend.'})


@bp.route('/send_friend_message', methods=["POST"])
def send_friend_message():
    prnt(request.form)
    user_tag = request.form.get('user_tag').strip()
    message = request.form.get('message').strip()
    if not user_tag:
        return jsonify({'success': False, 'message': 'No user tag was passed.'})
    user = get_user_from_tag(user_tag)
    if not user:
        return jsonify({'success': False, 'message': 'Could not find user with that tag'})
    user.send_message_to_user(str(current_user.id))
    return jsonify({'success': True, 'message': f'Sent message to friend'})

@bp.route('/get_friend_messages', methods=["POST"])
def get_friend_messages():
    prnt(request.form)
    user_tag = request.form.get('user_tag').strip()
    if not user_tag:
        return jsonify({'success': False, 'message': 'No user tag was passed.'})
    user = get_user_from_tag(user_tag)
    if not user:
        return jsonify({'success': False, 'message': 'Could not find user with that tag'})
    user_id = str(user.id)
    messages = current_user.get_friend_messages(user_id)

    return jsonify({'success': True, 'message': f'Successfully acquired friend messages', 'messages': messages})
