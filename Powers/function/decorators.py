from pyrogram import Client
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.enums import ChatType as CT
from pyrogram.filters import create
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

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
