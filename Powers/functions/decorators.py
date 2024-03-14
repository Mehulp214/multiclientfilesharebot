from pyrogram import Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType as CT
from pyrogram.filters import create
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from Powers.database.pending_request_db import REQUESTED_USERS
from Powers.functions.get_fsub_kb import get_fsub_kb
from Powers.functions.load_fsub import get_channels
from Powers.functions.supports import get_support_staff


def start_in_private(func):
    async def redirect(c: Client, m: Message):
        if m.chat.type != CT.PRIVATE:
            kb = IKM(
                [
                    [
                        IKB("Start me in Private",
                            url=f't.me/{c.me.username}?start=start')
                    ]
                ]
            )
            txt = "Start me in private"
            await m.reply_text(txt, reply_markup=kb)
            return
        else:
            user = m.from_user.id
            data = "start"
            if len(m.text.strip().split()) > 1:
                data = m.text.split(None, 1)[1]
            channels = get_channels(c.me.id)
            f_join = False
            for i in channels:
                channel = int(i['c_id'])
                if i['type'] == "request":
                    try:
                        u_status = await c.get_chat_member(channel, user)
                        if u_status.status in [CMS.ADMINISTRATOR, CMS.MEMBER, CMS.OWNER]:
                            continue
                        else:
                            reqq = REQUESTED_USERS(channel).get_pending_users(user)
                            if not reqq:
                                f_join = True
                                break
                    except Exception:
                        reqq = REQUESTED_USERS(channel).get_pending_users(user)
                        if not reqq:
                            f_join = True
                            break
                else:
                    try:
                        u_status = await c.get_chat_member(channel, user)
                        if u_status.status in [CMS.ADMINISTRATOR, CMS.MEMBER, CMS.OWNER]:
                            continue
                        else:
                            f_join = True
                            break
                    except Exception:
                        f_join = True
                        break

            if f_join:
                kb = await get_fsub_kb(c, data)
                await m.reply_text(
                    "Looks like you haven't joined all of the channels\nJoin them to continue",
                    reply_markup=kb
                )
                return
            else:
                return await func(c, m)
    return redirect


async def bot_owners(_, c: Client, m: Message):
    supports = get_support_staff(c.me.id)
    supports = supports + [c.owner.id]
    if m.from_user.id in supports:
        return True
    else:
        return False


async def restrict_check_func(_, __, m: Message):
    """Check if user can restrict users or not."""

    if (
        m.chat.type not in [CT.SUPERGROUP, CT.GROUP]
    ):
        return False

    if not m.from_user:
        return False

    user = await m.chat.get_member(m.from_user.id)

    if user and user.status in [CMS.ADMINISTRATOR, CMS.OWNER]:
        if user.privileges.can_restrict_members:
            status = True
        else:
            status = False
            await m.reply_text(text="You don't have permissions to restrict members!")
    else:
        await m.reply_text("You can't use admin commands")
        status = False

    return status

async def bot_admin_check(c: Client, chat):
    try:
        is_admin = await c.get_chat_member(chat, c.me.id)
    except:
        return False
    if is_admin.status in [CMS.ADMINISTRATOR, CMS.OWNER]: #don't ask me why owner?
        return True
    else:
        return False


bot_owner_filt = create(bot_owners)
restrict_filter = create(restrict_check_func)
