from flask import request, jsonify, current_app, render_template
from flask_login import current_user
from app.blueprints.friends import bp
from app.helpers.models import get_user_from_id, get_user_from_tag
from app.blueprints.friends.cache_helpers import get_sid_from_user_id
from app.blueprints.friends.sockets import emit_friend_request_to_sid
from slg_utilities.helpers import prnt

from app.blueprints.friends.test import TEST_PARTY_MESSAGES



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
    if isinstance(user, dict): # means we failed and are returning failure object
        return jsonify(user)

    user.add_to_friend_requests(str(current_user.id))
    sid = get_sid_from_user_id(str(user.id))
    emit_friend_request_to_sid(sid, current_user.user_tag, str(current_user.id))
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
    if isinstance(user, dict): # means we failed and are returning failure object
        return jsonify(user)
    result = current_user.send_message_to_user(message, str(user.id))
    return result
    # return jsonify({'success': True, 'message': f'Sent message to friend'})

@bp.route('/get_friend_messages', methods=["POST"])
def get_friend_messages():
    prnt(request.form)
    user_tag = request.form.get('user_tag').strip()
    if not user_tag:
        return jsonify({'success': False, 'message': 'No user tag was passed.'})
    user = get_user_from_tag(user_tag)
    if not user:
        return jsonify({'success': False, 'message': 'Could not find user with that tag'})
    if isinstance(user, dict): # means we failed and are returning failure object
        return jsonify(user)
    user_id = str(user.id)
    messages = current_user.get_friend_messages(user_id)

    return jsonify({'success': True, 'message': f'Successfully acquired friend messages', 'messages': messages})

@bp.route('/get_party_messages', methods=["GET"])
def get_party_messages():
    print('getting messages', flush=True)
    party = current_user.get_party()
    print(party)
    if party:
        messages = party.messages
    else:
        # messages = TEST_PARTY_MESSAGES
        messages = "not in party"

    return jsonify({'success': True, 'message': f'Successfully acquired friend messages', 'messages': messages})

@bp.route('/send_party_invite', methods=["POST"])
def send_party_invite():
    current_user.send_party_invite(request.form.get('user_id'))
    return jsonify({'success': True, 'message': f'Successfully acquired friend messages'})

@bp.route('/accept_party_invite', methods=["POST"])
def accept_party_invite():
    inviting_user = get_user_from_tag(request.form.get('user_tag'))
    current_user.accept_party_invite(str(inviting_user.id))
    return jsonify({'success': True, 'message': f''})

@bp.route('/decline_party_invite', methods=["POST"])
def decline_party_invite():
    current_user.decline_party_invite(request.form.get('user_tag'))
    return jsonify({'success': True, 'message': f'Successfully acquired friend messages'})