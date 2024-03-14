from datetime import datetime, timedelta

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors import (ChatAdminRequired, PeerIdInvalid, RightForbidden,
                             UserAdminInvalid, UserNotParticipant)
from pyrogram.types import ChatPermissions, Message

from Powers import LOGGER


async def extract_time(m: Message, time_val: str):
    """Extract time from message."""
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await m.reply("Unspecified amount of time.")
            return
        initial_time = datetime.now()
        if unit == "m":
            bantime = initial_time + timedelta(minutes=int(time_num))
        elif unit == "h":
            bantime = initial_time + timedelta(hours=int(time_num))
        elif unit == "d":
            bantime = initial_time + timedelta(days=int(time_num))
        else:
            # how even...?
            await m.reply_text("Unable to specify time duration...")
            return
        return bantime
    await m.reply(
        f"Invalid time type specified. Needed m, h, or s. got: {time_val[-1]}",
    )
    return


async def ban_user(c: Client, m: Message, till_date=None):
    if till_date:
        till_date = await extract_time(m, till_date)
        if not till_date:
            return

    try:
        if m.reply_to_message.from_user.id == m.from_user.id:
            await m.reply_text("You are dumb ass from the birth or just happend to be??")
            return
        if m.reply_to_message.from_user.id == c.me.id:
            await m.reply_text("NUH UH! I am not going to ban myself")
            return
        replied_user = await m.chat.get_member(m.reply_to_message.from_user.id)
        if replied_user.status == CMS.OWNER:
            await m.reply_text("I can't ban owner u brat!")
            return
        await m.chat.ban_member(m.reply_to_message.from_user.id, till_date)
        txt = f"Banned {m.reply_to_message.from_user.mention} from the {m.chat.title} by {m.from_user.mention}"
        if till_date:
            txt += f" till {till_date}"
        await m.reply_text(txt)
        return
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
        return
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
        return
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
        return
    except UserNotParticipant:
        await m.reply_text("User is not part of the group")
        return
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
        return
    except Exception as e:
        await m.reply_text(f"Failed to ban due to\n{e}")
        LOGGER.error(e)
        return


async def mute_user(c: Client, m: Message, till_date=None):
    if till_date:
        till_date = await extract_time(m, till_date)
        if not till_date:
            return

    try:
        if m.reply_to_message.from_user.id == m.from_user.id:
            await m.reply_text("You are dumb ass from the birth or just happend to be??")
            return
        if m.reply_to_message.from_user.id == c.me.id:
            await m.reply_text("NUH UH! I am not going to mute myself")
            return
        replied_user = await m.chat.get_member(m.reply_to_message.from_user.id)
        if replied_user.status == CMS.OWNER:
            await m.reply_text("I can't mute owner u brat!")
            return
        await m.chat.restrict_member(m.reply_to_message.from_user.id, ChatPermissions())
        txt = f"Muted {m.reply_to_message.from_user.mention} from the chat {m.chat.title} by {m.from_user.mention}"
        if till_date:
            txt += f" till {till_date}"
        await m.reply_text(txt)
        return
    except ChatAdminRequired:
        await m.reply_text(text="I'm not admin or I don't have rights.")
        return
    except PeerIdInvalid:
        await m.reply_text(
            "I have not seen this user yet...!\nMind forwarding one of their message so I can recognize them?",
        )
        return
    except UserAdminInvalid:
        await m.reply_text(
            text="Cannot act on this user, maybe I wasn't the one who changed their permissions."
        )
        return
    except UserNotParticipant:
        await m.reply_text("User is not part of the group")
        return
    except RightForbidden:
        await m.reply_text(text="I don't have enough rights to ban this user.")
        return
    except Exception as e:
        await m.reply_text(f"Failed to ban due to\n{e}")
        LOGGER.error(e)
        return


async def unrestrict_user(m: Message):
    try:
        await m.chat.unban_member(m.reply_to_message.from_user.id)
        await m.reply_text(
            f"Unbanned {m.reply_to_message.from_user.mention} in the chat {m.chat.title} by {m.from_user.mention}"
        )
    except Exception as e:
        await m.reply_text(f"Failed to ban due to\n{e}")
        LOGGER.error(e)


async def kick_user(c: Client, m: Message):
    till_date = datetime.now() + timedelta(minutes=5)
    try:
        if m.reply_to_message.from_user.id == m.from_user.id:
            await m.reply_text("You are dumb ass from the birth or just happend to be??")
            return
        if m.reply_to_message.from_user.id == c.me.id:
            await m.reply_text("NUH UH! I am not going to kick myself")
            return
        replied_user = await m.chat.get_member(m.reply_to_message.from_user.id)
        if replied_user.status == CMS.OWNER:
            await m.reply_text("I can't kick owner u brat!")
            return
        await m.chat.ban_member(m.reply_to_message.from_user.id, till_date)
        txt = f"Kicked {m.reply_to_message.from_user.mention} from the chat {m.chat.title} by {m.from_user.mention}\n**They will not be able to join this chat for 5 minutes**"
        await m.reply_text(txt)
    except Exception as e:
        await m.reply_text(f"Failed to ban due to\n{e}")
        LOGGER.error(e)
    return
