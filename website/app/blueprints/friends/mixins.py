from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from flask import current_app, jsonify

import mongoengine as me
from app.blueprints.friends.cache_helpers import get_sid_from_user_id
from app.blueprints.friends.sockets import emit_friend_message_to_sid, emit_party_invite_to_sid, emit_party_message_to_sid
from app.helpers.models import get_user_from_id, get_user_from_tag
from slg_utilities.helpers import prnt

from app.blueprints.friends.models import Party

class PartyMixin:

    party_id = me.StringField(default='')
    party_invitations = me.ListField()

    def __init__(self):
        pass

    def get_party(self):
        if self.party_id:
            print(self.party_id, flush=True)
            return Party.objects(id=self.party_id).first()
        else:
            return None

    def send_party_invite(self, user_id):
        # check if we are currently in party
        if self.party_id:
            party = self.get_party()

            # check if user is in party
            if user_id in party.members:
                return jsonify({'success': False, 'message': 'User is already in party'})

            if str(self.id) != party.leader:
                if party.settings.get('leader_invite_only'):
                    return jsonify({'success': False, 'message': 'Sending user not authorized to invite'})

            if party.size >= party.max_size:
                return jsonify({'success': False, 'message': 'Party is full'})

            user = get_user_from_id(user_id)
            if not user:
                return jsonify({'success': False, 'message': 'No user found with that ID'})

            # send invitation
            emit_party_invite_to_sid(self.user_tag, get_sid_from_user_id(user_id))

            # add invitation to users party invitations
            user.party_invitations.append({
                'user_id': user_id,
                'user_tag': user.user_tag,
                'mmr': party.mmr,
            })
            self.save()

            return jsonify({'success': True, 'message': 'Party invite sent successfully'})

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
        self.party_id = str(party.id)
        self.save()
        return party.add_member(inviting_user, str(self.id))

    def decline_party_invite(self, inviting_user_id):
        self.party_invitations = [inv for inv in self.party_invitations if inv['user_id'] != inviting_user_id]
        self.save()
        return jsonify({'success': True, 'message': 'Party invite declined successfully'})

    def send_party_message(self, message):
        party = self.get_party()
        if party:
            message_dict = party.add_message(str(self.id), message)
            if message_dict:
                print(party, flush=True)
                for member_id in party.members:
                    sid = get_sid_from_user_id(member_id)
                    print(sid, flush=True)
                    emit_party_message_to_sid(message_dict, sid)

                    # another option here is to have users join a specific room and emit to that room
                    # that would be more efficient than sending to everyone but would require a bit of extra work
                    # so I'm not doing that for now

            return jsonify({'success': True, 'message': f'Successfully sent message to party'})
        return jsonify({'success': False, 'message': 'You are not in a party.'}), 400

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
