from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()


class FSUBS(MongoDB):
    """
    class to store fsub channels in database
    request, direct
    """

    db_name = "fsub_channel"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def inser_fsub(self, channel_id, bot_id, type=None):
        """
        channeld_id: Int type id of the channel
        type: request, direct. request if you want request to join type fsub and direct if you want normal fsub.
        """
        curr = self.find_one({'c_id': channel_id, "bot_id": bot_id})
        if curr:
            return curr['type']
        else:
            if type:
                self.insert_one({"c_id": channel_id, "bot_id": bot_id, "type": type})
                return False
            else:
                return True

    def update_fsub_type(self, channel_id, type, bot_id):
        curr = self.find_one({'c_id': channel_id, "bot_id": bot_id})
        if curr:
            self.update({'c_id': channel_id, "bot_id": bot_id}, {"type": type})
            return True
        else:
            return False

    def remove_fsub(self, channel_id, bot_id):
        curr = self.find_one({'c_id': channel_id, "bot_id": bot_id})
        if curr:
            self.delete_one({'c_id': channel_id, "bot_id": bot_id})
        return

    def get_fsubs(self, bot_id, type="all"):
        """
        type: Type you want to fetch default to all.

        Types:
            direct: Fetch fsub channel which will directly accept the users.
            request: Fetch fsub channel with request to join attribute.
            all: Fetch bot type of channels

        all will return the list of dictionary of containing info of the channels insted of channel ids
        """
        if type == "request":
            all_ = self.find_all({'type': type, "bot_id":bot_id})
            curr = [int(i['c_id']) for i in all_]

        elif type == "direct":
            all_ = self.find_all({'type': type, "bot_id":bot_id})
            curr = [int(i['c_id']) for i in all_]

        else:
            curr = self.find_all({})

        return curr
