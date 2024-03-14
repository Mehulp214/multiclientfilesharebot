from Powers.database.forcesub_db import FSUBS
from Powers.vars import *


async def load_channels(bot_id):
    fsubss = FSUBS()
    for i in FSUB_CHANNEL:
        fsubss.inser_fsub(int(i), bot_id, "direct")
    for i in REQ_FSUB:
        fsubss.inser_fsub(int(i), bot_id, "request")


def get_channels(bot_id, type="all"):
    """
    type: Type you want to fetch default to all.

    Types:
        direct: Fetch fsub channel which will directly accept the users.
        request: Fetch fsub channel with request to join attribute.
        all: Fetch bot type of channels

    all will return the list of dictionary of containing info of the channels insted of channel ids
    """
    fsubss = FSUBS()

    if type not in ['all', 'request', 'direct']:
        return []
    else:
        return fsubss.get_fsubs(bot_id, type)
