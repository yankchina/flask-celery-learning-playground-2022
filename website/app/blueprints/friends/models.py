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
    leader = me.StringField(default='')
    max_size = me.IntField(default=8)
    datetime_created = me.DateTimeField(default=datetime.utcnow)
    datetime_disbanded = me.DateTimeField()
    members = me.ListField(default=[])
    messages = me.ListField(default=[])
    settings = me.DictField(default={
        'leader_invite_only': True,
    })
    blacklist = me.ListField(default=[])

    def __init__(self, leader_id):
        self.leader = leader_id
        self.save()

    @property
    def size(self):
        return len(self.members)

    @property
    def mmr(self):
        ''' Get this party's grouped mmr '''
        pass

    def add_member(self, sending_user, user_id):
        if sending_user != self.leader and self.settings.get('leader_invite_only'):
            return jsonify({'success': False, 'message': 'Sending user not authorized to invite'})
        user = get_user_from_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'No user found with that ID'})
        user_tag = user.user_tag
        self.members.append({
            'user_id': user_id,
            'user_tag': user_tag,
            'mmr': user.mmr,
        })
        self.save()
        return jsonify({'success': True, 'message': 'User added to party successfully'})

    def remove_member(self, user_id):
        self.members = [mem for mem in self.members if mem['user_id'] != user_id]
        if not self.members:
            self.datetime_disbanded = datetime.utcnow()
        if self.leader == user_id:
            self.leader = self.members[0]['user_id']
        self.save()
        return jsonify({'success': True, 'message': 'User removed from party successfully'})

    def add_message(self, user_id, message):
        user = get_user_from_id(user_id)
        tag = user.user_tag
        self.messages.append({
            'user_tag': tag,
            'message': message,
        })
        self.save()
        return jsonify({'success': True, 'message': 'Message added'})
