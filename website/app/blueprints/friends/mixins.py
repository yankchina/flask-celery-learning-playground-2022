from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from flask import current_app, jsonify

import mongoengine as me
from app.blueprints.friends.cache_helpers import get_sid_from_user_id
from app.blueprints.friends.sockets import emit_friend_message_to_sid, emit_party_invite_to_sid
from app.helpers.models import get_user_from_id, get_user_from_tag
from slg_utilities.helpers import prnt

from app.blueprints.friends.models import Party

class PartyMixin:

    party_id = me.StringField(default='')

    def __init__(self):
        pass

    def get_party(self):
        if self.party_id:
            return Party.objects.get(id=self.party_id)
        else:
            return None

    def send_party_invite(self, user_id):
        # check if we are currently in party
        if self.party_id:
            party = self.get_party()

            # check if user is in party
            if user_id in party.members:
                return jsonify({'success': False, 'message': 'User is already in party'})

            if self.user_id != party.leader:
                if party.settings.get('leader_invite_only'):
                    return jsonify({'success': False, 'message': 'Sending user not authorized to invite'})

            if party.size >= party.max_size:
                return jsonify({'success': False, 'message': 'Party is full'})

            user = get_user_from_id(user_id)
            if not user:
                return jsonify({'success': False, 'message': 'No user found with that ID'})

            # send invitation
            emit_party_invite_to_sid(self.user_tag, get_sid_from_user_id(user_id))

        else:
            # create a new party and make ourselves the leader
            party = Party(str(self.id))
            self.party_id = str(party.id)
            self.save()
            self.send_party_invite(user_id)

    def accept_party_invite(self, inviting_user_id):
        if self.party_id:
            return jsonify({'success': False, 'message': 'User is already in party'})

        inviting_user = get_user_from_id(inviting_user_id)
        party = inviting_user.get_party()
        return party.add_member(inviting_user, str(self.id))

    def send_party_message(self, message):
        pass

class FriendsMixin:
    friends_list = me.ListField(default=[])
    friend_messages = me.DictField(default={})
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
        if friend_id in self.friend_messages:
            return self.friend_messages[friend_id]
        else:
            return []

    def add_to_friend_messages(self, message, user_id, who, time):
        if user_id not in self.friend_messages:
            self.friend_messages[user_id] = []
        self.friend_messages[user_id].append({
            'message':message,
            'time':time,
            'who': who, # self or friend
        })
        self.save()

    def send_message_to_user(self, message, user_id, depth=0):
        friend = get_user_from_id(user_id)
        if str(friend.id) in self.friends_list:
            if depth == 0:
                who = 'self'
            else:
                who = 'friend'
            self.add_to_friend_messages(message, user_id, who, datetime.now())
            if depth == 0:
                # send the message back to ourself, but without the emit
                friend.send_message_to_user(message, str(self.id), depth=1)
                emit_friend_message_to_sid(self.user_tag, message, get_sid_from_user_id(user_id))
                return jsonify({'success': True, 'message': f'Sent message to friend'})
        else:
            return jsonify({'success': False, 'message': 'User not in friends list'})

    def get_recent_friends_contacted(self, num_days=14):
        '''
        Return a list of user_ids of friends who have been contacted in the last num_days days.
        '''
        now = datetime.now()
        cutoff = now - timedelta(days=num_days)
        friends = []
        for friend in self.friends_list:
            if friend in self.friend_messages and self.friend_messages[friend][-1]['time'] > cutoff:
                friends.append(friend)
        return friends
