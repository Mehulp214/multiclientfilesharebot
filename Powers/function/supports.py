from Powers.database.support_db import SUPPORTS


async def load_support_users(bot_id, sudo):
    support = SUPPORTS()
    support.insert_support_user(bot_id, sudo)


def get_support_staff(bot_id: int):
    support = SUPPORTS()
    sudo = support.get_support(bot_id)
    return sudo
