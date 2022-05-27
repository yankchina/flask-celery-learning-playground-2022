from flask import jsonify
from datetime import datetime
import mongoengine as me
from flask import current_app
from flask_login import UserMixin
import app.models.party as p
import app.blueprints.matchmaking.models as m




class UnregisteredUser(UserMixin, me.Document, p.PartyMixin, m.MatchmakingMixin):
    # meta = { 'collection': cfg.get('UNREGISTERED_USERS_COLLECTION'), 'strict': False}
    meta = {'strict': False}
    username = me.StringField(min_length=3, max_length=16)
    unregistered_tag = me.StringField()
    mmr = me.IntField(default=1000)
    datetime_joined_queue = me.DateTimeField()
    party_id = me.StringField()
    in_game_id = me.ListField()
    doodl_coins = me.IntField(default=100)
    notifications = me.DictField()
    settings = me.DictField()
    call_counts = me.DictField()
    counts = me.DictField()
    member_since = me.DateTimeField(default=datetime.utcnow)
    last_seen = me.DateTimeField(default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(UnregisteredUser, self).__init__(**kwargs)
        self.unregistered_tag = str(self.id)[-4:]

    def update_username(self, username):
        self.username = username
        self.save()

    def can_join_party(self):
        return False if self.party_id else True

    def to_json(self):
        json_user = {
            'username': self.username,
            'tag': self.unregistered_tag,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'datetime_joined_queue': self.datetime_joined_queue,
            'DoodlCoins': self.doodl_coins,
            'settings': self.settings,
        }
        return json_user

    def __repr__(self):
        return f'<UnregisteredUser {self.username}#{self.unregistered_tag}>'

    def __str__(self):
        base_string = [f'{key}: {value}\n' for key,
                       value in self.to_json().items()]
        return 'User\n' + ''.join(base_string)