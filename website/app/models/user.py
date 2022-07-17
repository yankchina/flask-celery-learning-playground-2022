from datetime import datetime
import mongoengine as me
from flask import current_app

# from .party import PartyMixin
# import app.models.party as p
import app.blueprints.matchmaking.models as m
import app.blueprints.friends.mixins as f

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import jwt
from time import time




class User(UserMixin, me.Document, f.PartyMixin, m.MatchmakingMixin, f.FriendsMixin):
    # meta = { 'collection': cfg.get('USERS_COLLECTION'), 'strict': False}
    meta = {'strict': False}
    username = me.StringField(min_length=3, max_length=16)
    username_lower = me.StringField(min_length=3, max_length=16, unique=True)
    user_tag = me.StringField()
    email = me.EmailField(required=True, unique=True)
    email_verified = me.BooleanField(default=False)
    password_hash = me.StringField(required=True)
    party_id = me.StringField()
    games_left = me.ListField()
    games_in = me.ListField()
    doodl_coins = me.IntField(default=100)
    notifications = me.DictField()
    settings = me.DictField()
    call_counts = me.DictField()
    counts = me.DictField()
    member_since = me.DateTimeField(default=datetime.utcnow)
    last_seen = me.DateTimeField(default=datetime.utcnow)

    mmr = me.IntField(default=1000)
    datetime_joined_queue = me.DateTimeField()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.user_tag = self.username

    def can_join_party(self):
        return False if self.party_id else True

    def get_matchmaking_info(self):
        info = {
            'id': self._id,
            'mmr': self.mmr,
        }
        return info

    def to_json(self):
        json_user = {
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'settings': self.settings,
        }
        return json_user

    def __str__(self):
        base_string = [f'{key}: {value}\n' for key,
                       value in self.to_json().items()]
        return 'User\n' + ''.join(base_string)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def generate_confirmation_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'confirm': str(self.id)}).decode('utf-8')

    # def confirm(self, token):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     user = User.query.get(data.get('confirm'))
    #     if user is None:
    #         return False
    #     self.email_confirmed = True
    #     me.save()
    #     return True

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)