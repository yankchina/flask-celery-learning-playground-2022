from datetime import datetime


class MatchmakingMixin:
    '''
    This requires these properties in the parent class:

        mmr = me.IntField(default=1000)
        datetime_joined_queue = me.DateTimeField()

    '''
    def join_queue(self):
        if not self.datetime_joined_queue:
            self.datetime_joined_queue = datetime.utcnow()
            self.save()
            return True
        return False

    def leave_queue(self):
        self.datetime_joined_queue = None
        self.save()
        return True

    def get_seconds_since_joined_queue(self):
        if self.datetime_joined_queue:
            return (datetime.utcnow() - self.datetime_joined_queue).seconds + 1

    def reset_matchmaking(self):
        self.datetime_joined_queue = None
        self.save()

    def get_matchmaking_info(self):
        info = {
            'id': str(self.id),
            'mmr': self.mmr,
        }
        return info
