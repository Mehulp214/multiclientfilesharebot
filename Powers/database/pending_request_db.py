from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()


class REQUESTED_USERS(MongoDB):
    """
    class to store join requested users in database
    """

    db_name = "pending_request"

    def __init__(self, channel: int) -> None:
        super().__init__(self.db_name)
        self.channel = channel

    def insert_pending_user(self, user: int):
        curr = self.find_one({'c_id': self.channel, 'user': user})
        if curr:
            return
        else:
            self.insert_one({'c_id': self.channel, 'user': user})

    def remove_pending_user(self, user: int):
        curr = self.find_one({'c_id': self.channel, 'user': user})
        if not curr:
            self.delete_one({'c_id': self.channel, 'user': user})
        return

    def get_pending_users(self, user=None):
        """
        if user id is not given it will return list of all pending requests in the channel
        """
        if not user:
            curr = self.find_all({'c_id': self.channel})
            user = [i['user'] for i in curr]

        else:
            curr = self.find_one({'c_id': self.channel, 'user': user})
            if not curr:
                return False
            user = True

        return user
