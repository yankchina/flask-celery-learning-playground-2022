from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from flask import current_app, jsonify

import mongoengine as me
from app.blueprints.friends.cache_helpers import get_sid_from_user_id
from app.blueprints.friends.sockets import emit_friend_message_to_sid
from app.helpers.models import get_user_from_id
from slg_utilities.helpers import prnt


class Party(me.Document):
    leader = me.StringField()
    max_size = me.IntField(default=8)
    datetime_created = me.DateTimeField(default=datetime.utcnow)
    datetime_disbanded = me.DateTimeField()
    members = me.ListField(default=[])
    messages = me.ListField(default=[])
    settings = me.DictField(default={
        'leader_invite_only': True,
    })
    blacklist = me.ListField(default=[])

    @classmethod
    def init_with_leader_id(cls, leader_id):
        party = cls()
        party.leader = leader_id
        user = get_user_from_id(leader_id)
        party.members.append({
            'user_id': leader_id,
            'user_tag': user.user_tag,
            'mmr': user.mmr,
        })
        party.save()
        return party

    @property
    def size(self):
        return len(self.members)

    @property
    def sid(self):
        # can change in the future but we will always use sid as the accessor
        return str(self.id)

    @property
    def mmr(self):
        ''' Get this party's grouped mmr '''
        pass

    def add_member(self, sending_user, user_id):
        try:
            if str(sending_user.id) != self.leader and self.settings.get('leader_invite_only'):
                return {'success': False, 'message': 'Party is currently set to leader invite only.'}
            user = get_user_from_id(user_id)
            if not user:
                return {'success': False, 'message': 'No user found with that ID'}
            user_tag = user.user_tag
            self.members.append({
                'user_id': user_id,
                'user_tag': user_tag,
                'mmr': user.mmr,
            })
            self.save()
            return {'success': True, 'message': f'{user.user_tag} joined the party.', 'party_sid': self.sid}
        except:
            return {'success': False, 'message': f'Failed to add user to party for unknown reason.'}

    def remove_member(self, user_id):
        self.members = [mem for mem in self.members if mem['user_id'] != user_id]
        if not self.members:
            self.datetime_disbanded = datetime.utcnow()
        if self.leader == user_id:
            self.leader = self.members[0]['user_id']
        self.save()
        return {'success': True, 'message': 'Left party.', 'party_sid': self.sid}

    def add_message(self, user_id, message):
        try:
            user = get_user_from_id(user_id)
            tag = user.user_tag
            message_dict = {
                'user_tag': tag,
                'message': message,
            }
            self.messages.append(message_dict)
            self.save()
            return message_dict
        except:
            return None

    def __repr__(self):
        member_string = '\n\t'.join([mem['user_tag'] for mem in self.members])
        return f'''
Leader: {self.leader}
ID: {self.id}
Members:
    {member_string}

Message Count: {len(self.messages)}
'''

    def __str__(self):
        member_string = '\n\t'.join([mem['user_tag'] for mem in self.members])
        return f'''
Leader: {self.leader}
ID: {self.id}
Members:
    {member_string}

Message Count: {len(self.messages)}
'''