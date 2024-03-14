from typing import List

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM

from Powers import LOGGER
from Powers.functions.load_fsub import get_channels


async def orgainzed_kb(kbs: List[IKB], rows: int = 2) -> List[List[IKB]]:
    """
    kbs: List of inlinekeyboardbutton
    rows: How many rows you want default to 2
    """
    new_kb = [kbs[i: i + rows] for i in range(0, len(kbs), rows)]
    return new_kb


async def get_fsub_kb(c: Client, data: str = "start") -> List[IKM]:
    """
    data: Either base 64 of the file you want to give after joining the channels or just start if the user is starting the bot for first time
    """
    try:
        all_fsubs = get_channels()

        fsub_join_links = []

        for i, j in enumerate(all_fsubs):
            channel = int(j['c_id'])
            if j["type"] == "request":
                invite_link = await c.create_chat_invite_link(channel, creates_join_request=True)
            else:
                invite_link = await c.create_chat_invite_link(channel)

            fsub_join_links.append(IKB(f"Join Channel {i+1}", url=invite_link.invite_link))

        orgainzed = await orgainzed_kb(fsub_join_links)
        orgainzed.append(
            [IKB(f"Restart ⚡️", url=f't.me/{c.me.username}?start={data}')])

        return IKM(orgainzed)

    except Exception as e:
        LOGGER.error(e)
