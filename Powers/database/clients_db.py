from threading import RLock

from Powers.database import MongoDB

INSERTION_LOCK = RLock()


class CLIENTS(MongoDB):
    """
    class to store clients
    """

    db_name = "clients"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def load_client(self, bot_token: str, owner: int, db_channel: int, bot_id: int = 18):
        curr = self.find_one({"bot_id": bot_id})
        if curr:
            return False
        else:
            self.insert_one(
                {
                    "bot_id": bot_id,
                    "bot_token": bot_token,
                    "owner_id": owner,
                    "db_channel": db_channel
                }
            )
            return True

    def remove_cliet(self, bot_id: int):
        curr = self.find_one({"bot_id": bot_id})
        if curr:
            self.delete_one({"bot_id": bot_id})
        return

    def get_client_info(self, bot_id: int):
        curr = self.find_one({"bot_id": bot_id})
        if curr:
            return curr
        else:
            return False

    def update_bot_token(self, bot_id: int, bot_token: str):
        curr = self.find_one({"bot_id": bot_id})
        if curr:
            self.update({"bot_id": bot_id}, {"bot_toekn": bot_token})
        return

    def update_bot_id(self, bot_id: int, bot_token: str):
        curr = self.find_one({"bot_token": bot_token})
        if curr and curr['bot_id'] == 18:
            self.update({"bot_token": bot_token}, {"bot_id": bot_id})
        return

    def get_all_clients(self):
        curr = self.find_all({})
        if curr:
            clients = curr
        else:
            clients = []
        return clients

    def get_clients_by_id(self, owner_id):
        curr = self.find_all({"owner_id":owner_id})
        if curr:
            return curr
        else:
            return []

    def get_db_channel(self, bot_id):
        curr = self.find_one({"bot_id": bot_id})
        if curr:
            return curr["db_channel"]
        return False

    def update_db_channel(self, bot_id, chat_id):
        curr = self.find_one({"bot_id":bot_id})
        if curr:
            self.update({"bot_id":bot_id},{"db_channel":chat_id})
