import mongoengine as me
from flask import current_app
# from flask_login import UserMixin, AnonymousUserMixin
# from app.models.user import User

# these are defined at bottom
# import app.models.user as u
# import app.models.unregistered_user as uu



# class PartyMixin:
#     def party_size(self):
#         if isinstance(self, Party):
#             return len(self.users)
#         # if isinstance(self, GenericUser):
#         if isinstance(self, u.User) or isinstance(self, uu.UnregisteredUser):
#             return 1

#     def party_users(self):
#         if isinstance(self, Party):
#             return self.users
#         # if isinstance(self, GenericUser):
#         if isinstance(self, u.User) or isinstance(self, uu.UnregisteredUser):
#             return [str(self.id)]


class Party(me.Document, PartyMixin):
    # meta = {'collection': cfg.get('PARTIES_COLLECTION'), 'strict': False}
    meta = {'strict': False}
    name = me.StringField()
    password = me.StringField()
    leader = me.StringField()  # user_id of leader
    users = me.DictField()  # user_id: username
    banned_users = me.ListField()
    games_left = me.ListField()

    def __init__(self, **kwargs):
        super(Party, self).__init__(**kwargs)

    @classmethod
    def create_party(cls):
        party = Party()
        party.save()
        return party

    @classmethod
    def delete_party(cls, id):
        return Party.objects(id=id).first().delete()

    def party_size(self):
        return len(self.users)

    def change_name(self, name):
        self.name = name
        self.save()

    def to_json(self):
        json = {key: value for key, value in self._data.items() if key != 'id'}
        json['id'] = str(self.id)
        return json

    def add_user(self, user_id):
        user_id = str(user_id)
        if user_id in self.banned_users:
            return 'User is banned from this party'

        user = User.objects(id=user_id).first()
        if not user:
            user = UnregisteredUser.objects(id=user_id).first()
        # user = GenericUser.objects(id=user_id).first()
        if user:
            if user.can_join_party():
                user.party_id = str(self.id)
                self.users[user_id] = user.username
                if not self.leader:
                    self.leader = user_id

                self.save()
                return f'{user.username} successfully added to party "{self.name}"'
        else:
            return 'No user found with that ID'

    def remove_user(self, user_id, ban=False):
        user_id = str(user_id)
        del self.users[user_id]

        if len(self.users) < 1:
            return self.delete()

        # assign leadership to earliest member
        if self.leader == user_id:
            self.leader = self.users.keys()[0]

        if ban:
            self.banned_users.append(user_id)

        self.save()
        return f'Successfully removed {user_id}'

    def can_join_game(self, game_size=8):
        if self.party_size > game_size:
            return False

    def find_game(self):
        pass

    def join_game(self, game=None, game_id=None):
        # at this point we will assume all checks have been made and that we can add the users, no problem
        # if the game has been established already, which it likely has, we can accept that, or if we are joining blind then just pass the game_id
        pass

    def leave_game(self, game_id, bring_users=True):
        pass

import app.models.user as u
import app.models.unregistered_user as uu