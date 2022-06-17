from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from flask import current_app, jsonify

import mongoengine as me
from app.blueprints.friends.cache_helpers import get_sid_from_user_id
from app.blueprints.friends.sockets import emit_friend_message_to_sid
from app.helpers.models import get_user_from_id


class FriendsMixin:
    '''
    This requires these properties in the parent class:

        friends_list = me.ListField(default=[])
        friend_messages = me.ListField(default=[])
        friend_requests = me.ListField(default=[])
        blocked_users = me.ListField(default=[])
        recently_played_with = me.ListField(default=[])
    '''
    friends_list = me.ListField(default=[])
    friend_messages = me.ListField(default=[])
    friend_requests = me.ListField(default=[])
    blocked_users = me.ListField(default=[])
    recently_played_with = me.ListField(default=[])

    def __init__(self):
        pass

    def add_friend(self, user_id: str):
        try:
            if user_id in self.friends_list:
                return False
            self.friends_list.append(user_id)
            self.remove_from_friend_requests(user_id, save=False)
            self.save()
            return True
        except:
            current_app.exception('Unknown exception adding friend to friends list.')
        return False

    def remove_friend(self, user_id, depth=0, save=True):
        if user_id in self.friends_list:
            try:
                self.friends_list = [friend for friend in self.friends_list if friend != user_id]

                if depth == 0:
                    # remove ourself from our friends list too
                    friend = get_user_from_id(user_id)
                    friend.remove_friend(str(self.id), depth=1)

                if save:
                    self.save()
                return True
            except:
                current_app.exception('Unknown exception removing friend from friends list.')
        return False

    def block_user(self, user_id):
        pass

    def add_to_friend_requests(self, user_id, save=True):
        self.friend_requests.append(user_id)
        if save:
            self.save()
        return True

    def remove_from_friend_requests(self, user_id, save=True):
        self.friend_requests = [id_ for id_ in self.friend_requests if id_ != user_id]
        if save:
            self.save()
        return True

    def get_friend_messages(self, friend_id, sort=True):
        output = list(filter(lambda msg: msg['user_id'] == friend_id, self.friend_messages))
        return sorted(output, key=lambda msg: msg['time']) if sort else output

    def get_friend_message_dict(self, sort_by="datetime"):
        '''
        Return object

            {user_id: {
                'username': friend_username,
                'messages': list_of_messages of type FriendMessage sorted by datetime
            },
                ...
            }
        '''
        message_dict = {}
        for msg in self.friend_messages:
            if msg.user_id not in message_dict:
                message_dict[msg['user_id']] = {'messages': [], 'user_tag': get_user_from_id(msg['user_id']).user_tag}

            message_dict[msg['user_id']]['messages'].append({
                'message': msg['message'],
                'time': msg['time']
            })

        if sort_by == 'datetime':
            for id_ in message_dict:
                message_dict[id_]['messages'] = sorted(message_dict[id_]['messages'], key=lambda msg: msg['time'])

        return message_dict

    def add_to_friend_messages(self, message, user_id, time):
        self.friend_messages.append(FriendMessage(
            user_id=user_id,
            message=message,
            time=time
        ))
        self.save()

    def send_message_to_user(self, message, user_id, depth=0):
        friend = get_user_from_id(user_id)
        if friend in self.friends_list:
            self.add_to_friend_messages(message, user_id, datetime.now())
            if depth == 0:
                # send the message back to ourself, but without the emit
                friend.send_message_to_user(message, str(self.id), depth=1)
                emit_friend_message_to_sid(message, get_sid_from_user_id(user_id))
        else:
            return jsonify({'success': False, 'message': 'User not in friends list'})


@dataclass
class FriendMessage:
    user_id: str
    message: str
    time: datetime