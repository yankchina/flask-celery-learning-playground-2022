from flask_login import login_required, current_user
from app.blueprints.friends import bp
from slg_utilities.helpers import prnt

from app.helpers.models import get_user_from_id

@bp.app_context_processor
def inject_friends_list():
    friends_list = []
    for user_id in current_user.friends_list:
        user = get_user_from_id(user_id)
        player_info = {'username': user.username, 'user_id': str(user.id), 'user_tag': user.user_tag, 'user_type': user._cls}
        if user._cls == 'UnregisteredUser':
            player_info['tag'] = user.unregistered_tag
        friends_list.append(player_info)
    return dict(friends_list=friends_list)

@bp.app_context_processor
def inject_friend_requests():
    friend_requests = []
    prnt(current_user)
    for user_id in current_user.friend_requests:
        user = get_user_from_id(user_id)
        player_info = {'username': user.username, 'user_id': str(user.id), 'user_tag': user.user_tag, 'user_type': user._cls}
        if user._cls == 'UnregisteredUser':
            player_info['tag'] = user.unregistered_tag
        friend_requests.append(player_info)
        prnt(friend_requests)
    return dict(friend_requests=friend_requests)

@bp.app_context_processor
def inject_blocked_users():
    blocked_users = []
    for user_id in current_user.blocked_users:
        user = get_user_from_id(user_id)
        blocked_users.append({'username': user.username, 'user_tag': user.user_tag, 'user_type': user._cls})
    return dict(blocked_users=blocked_users)

@bp.app_context_processor
def inject_recently_played_with():
    recently_played_with = []
    for user_id in current_user.recently_played_with:
        user = get_user_from_id(user_id)
        recently_played_with.append({'username': user.username, 'user_tag': user.user_tag, 'user_type': user._cls})
    return dict(recently_played_with=recently_played_with)

@bp.app_context_processor
def inject_user_tag():
    return dict(user_tag=current_user.user_tag)

@bp.app_context_processor
def inject_recent_friends_contacted():
    friend_ids = current_user.get_recent_friends_contacted(num_days=7)
    user_tags = [get_user_from_id(friend_id).user_tag for friend_id in friend_ids]
    return dict(recent_friends_contacted=user_tags)

@bp.app_context_processor
def inject_friend_party_invites():
    return dict(friend_party_invitations=current_user.party_invitations)