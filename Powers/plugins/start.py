from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from Powers import LOGGER
from Powers.functions.decorators import start_in_private
from Powers.functions.encode_decode import encoder
from Powers.plugins import *


@Client.on_message(filters.command("start"))
@start_in_private
async def is_bot_start(c: Client, m: Message):
    kb = IKM(
        [
            [
                IKB("Help", "get.help"),
            ],
            [
                IKB("Owner", user_id=c.owner.id)
            ]
        ]
    )
    txt = f"Hi {m.from_user.mention if m.from_user else m.chat.title}!\nMy self {c.me.first_name}\nI am a file sharer bot with some basic admin commands.\n**Want to deploy your own bot like me?**\nJust type `/deployown` to know how you can do so."
    if len(m.text.strip().split()) > 1:
        data = m.text.split(None, 1)[1]
        if data == "start":
            await m.reply_text(txt, reply_markup=kb)
            return
        elif data.startswith("get_"):
            db_chat_id = c.db_channel.id
            curr_id = m.chat.id
            b64_str = data.split("_", 1)
            decoded = (await encoder(b64_str[1], "decode")).split("-")
            if len(decoded) > 1:
                from_msg = int(decoded[0])
                to_msg = int(decoded[1])
                msgs = range(from_msg, to_msg+1)
                MSGS: list[Message] = []
                for msg in msgs:
                    try:
                        msg_t = await c.get_messages(db_chat_id, int(msg))
                        MSGS.append(msg_t)
                    except Exception as e:
                        LOGGER.error(e)
                        continue

                for i in MSGS:
                    try:
                        await i.copy(curr_id, protect_content=True)
                    except Exception as e:
                        LOGGER.error(e)
                        break
                await m.reply_text("Here are your all requested Client")
                return
            else:
                msg = decoded[0]
                try:
                    MSG = await c.get_messages(db_chat_id, int(msg))
                    await MSG.copy(curr_id, protect_content=True)
                    await m.reply_text("Here is your requested file")
                    return
                except Exception as e:
                    LOGGER.error(e)
                    return

    await m.reply_text(txt, reply_markup=kb)
    return


@Client.on_message(filters.command("help"))
@start_in_private
async def what_can_I_do(c: Client, m: Message):
    kb = IKM(
        [
            [
                IKB("Deploy", "get.deployOwn"),
                IKB("Back", "get.main")
            ]
        ]
    )
    if c.is_main:
        txt = main_help_txt
    else:
        txt = other_help_txt

    await m.reply_text(txt, reply_markup=kb)
