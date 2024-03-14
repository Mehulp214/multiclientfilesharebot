from threading import RLock
from typing import List

from Powers.database import MongoDB

INSERTION_LOCK = RLock()


class SUPPORTS(MongoDB):
    """
    class to store support users in database
    sudo
    """

    db_name = "supports"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def insert_support_user(self, bot_id: int, user_id: List[int]):
        curr = self.find_one({"bot_id":bot_id})
        if not curr:
            with INSERTION_LOCK:
                self.insert_one(
                    {
                        "bot_id": bot_id,
                        "sudo": user_id
                    }
                )
            return

    def update_support(self, bot_id: int, user_id: int):
        curr = self.find_one({"bot_id":bot_id})
        if curr:
            supp = self.get_support(bot_id)
            supp = supp.append(user_id)
            self.update({"bot_id":bot_id}, {"sudo": list(set(supp))})
        return


    def is_support_user(self, bot_id:int, user_id:int):
        curr = self.find_one({"bot_id": bot_id})
        if user_id in curr['sudo']:
            return curr['sudo']
        return False

    def delete_support_user(self, bot_id:int, user:int):
        curr = self.get_support(bot_id)
        if curr:
            with INSERTION_LOCK:
                new = curr.remove(user)
                self.update({"bot_id":bot_id},{'sudo':new})
        return

    def get_support(self, bot_id: int):
        curr = self.find_one({"bot_id":bot_id})
        if curr:
            return [int(i) for i in curr['sudo']]
        else:
            return []
