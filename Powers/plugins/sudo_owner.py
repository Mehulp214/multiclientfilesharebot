from os import execvp
from sys import executable

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from Powers import LOGGER
from Powers.core import app
from Powers.database.clients_db import CLIENTS
from Powers.database.support_db import SUPPORTS
from Powers.functions.decorators import bot_owner_filt, start_in_private
from Powers.functions.encode_decode import encoder
from Powers.functions.kb_helpers import orgainzed_kb


async def get_client_name_from_id(bot_id: int):
    for i in app.other:
        if i.me.id == bot_id:
            return i.me.first_name
    return

@Client.on_message(filters.command("restart") & bot_owner_filt)
async def restart_all_bots(c: Client, m: Message):
    if not c.is_main:
        return

    await m.reply_text("Restarting all bots...")
    execvp(executable, [executable, "-m", "Powers"])


@Client.on_message(filters.command("deletebot") & bot_owner_filt)
@start_in_private
async def delete_my_bot(c: Client, m: Message):
    owner = m.from_user
    clients = CLIENTS().get_clients_by_id(owner.id)
    txt = "Which of your bot you wanted to delete?"
    kb = []
    for client in clients:
        bot_name = await get_client_name_from_id(client['bot_id'])
        if not bot_name:
            continue
        kb.append(IKB(f"{bot_name}", f"delete:{client['bot_id']}"))
    if not kb:
        await m.reply_text("You have not deployed any bot")
        return
    orgainzed = await orgainzed_kb(kb)
    orgainzed.append([IKB("Delete all", f"delete_all:{owner.id}")])
    await m.reply_text(txt, reply_markup=IKM(orgainzed))
    return


@Client.on_message(filters.command("stopmybot") & bot_owner_filt)
@start_in_private
async def stop_my_bot(c: Client, m: Message):
    owner = m.from_user
    clients = CLIENTS().get_clients_by_id(owner.id)
    txt = "Which of your bot you wanted to stop?"
    kb = []
    for client in clients:
        for i in app.other:
            if int(client["bot_id"]) == i.me.id:
                kb.append(IKB(f"{i.me.first_name}", f"stop:{i.me.id}"))

    if not kb:
        await m.reply_text("You have not deployed any bot")
        return
    orgainzed = await orgainzed_kb(kb)

    orgainzed.append([IKB("Stop all", f"stop_all:{owner.id}")])

    await m.reply_text(txt, reply_markup=IKM(orgainzed))
    return


@Client.on_message(filters.command("startmybot") & bot_owner_filt)
@start_in_private
async def start_my_bot(c: Client, m: Message):
    owner = c.owner
    clients = CLIENTS().get_clients_by_id(owner.id)
    txt = "Which of your bot you wanted to start?"
    kb = []
    for client in clients:
        for i in app.other:
            if i.me.id == int(client["bot_id"]):
                continue
            else:
                kb.append(IKB(f"{i.me.first_name}", f"start:{client['bot_id']}"))

    if not kb:
        await m.reply_text("You have not deployed any bot")
        return
    orgainzed = await orgainzed_kb(kb)

    await m.reply_text(txt, reply_markup=IKM(orgainzed))
    return


@Client.on_message(filters.command("addsudo") & bot_owner_filt)
async def add_this_user_to_sudo(c: Client, m: Message):
    repl_to = m.reply_to_message
    if not repl_to:
        await m.reply_text("Reply to an user to add him in sudo")
        return

    elif repl_to and not repl_to.from_user:
        await m.reply_text("Reply to an user to add him in sudo")
        return

    else:
        user = repl_to.from_user.id
        SUPPORTS().update_support(c.me.id, user)
        await m.reply_text(f"Added {repl_to.from_user.mention} to support staff")
        return


@Client.on_message(filters.command("rmsudo") & bot_owner_filt)
async def remove_this_user_to_sudo(c: Client, m: Message):
    if m.from_user.id != c.owner.id:
        await m.reply_text("Only owner of the bot can remove user from sudo")
        return
    repl_to = m.reply_to_message

    if not repl_to:
        await m.reply_text("Reply to an user to add him in sudo")
        return

    elif repl_to and not repl_to.from_user:
        await m.reply_text("Reply to an user to add him in sudo")
        return

    else:
        user = repl_to.from_user
        SUPPORTS().delete_support_user(c.me.id, user.id)
        await m.reply_text(f"Removed {user.mention} from support")
        return


@Client.on_message(filters.command("getfilelink") & bot_owner_filt)
@start_in_private
async def get_file_encoded_link(c: Client, m: Message):
    requested = await c.ask(m.chat.id, "Give me the link of the file\nType /cancel to cancel the process", filters.text, timeout=120)
    if requested.text == "/cancel":
        await m.reply_text("Stopped the current process")
        return
    else:
        try:
            mess_id = int(requested.text.rsplit("/", 1)[-1])
            mess = await c.get_messages(c.db_channel.id, mess_id)
            mess_id = mess.id
            encoded = await encoder(mess_id)
            link = f"t.me/{c.me.username}?start=get_{encoded}"
            await m.reply_text(f"Here is your link `{link}`")
            return
        except ValueError:
            await m.reply_text("Invalid link")
            return
        except Exception as e:
            LOGGER.error(e)
            await m.reply_text(e)
            return


@Client.on_message(filters.command("getbatch") & bot_owner_filt)
@start_in_private
async def get_file_encoded_batch_link(c: Client, m: Message):
    requested = await c.ask(m.chat.id, "Give me the link of the first file you want to send\nType /cancel to cancel the process", filters.text, timeout=120)
    if requested.text == "/cancel":
        await m.reply_text("Stopped the current process")
        return
    else:
        try:
            mess_id = int(requested.text.rsplit("/", 1)[-1])
            mess = await c.get_messages(c.db_channel.id, mess_id)
            mess_id_1 = mess.id
            requested = await c.ask(m.chat.id, "Give me the link of the last file you want to send\nType /cancel to cancel the process", filters.text, timeout=120)
            if requested.text == "/cancel":
                await m.reply_text("Stopped the current process")
                return
            else:
                mess_id = int(requested.text.rsplit("/", 1)[-1])
                mess = await c.get_messages(c.db_channel.id, mess_id)
                mess_id_2 = mess.id
            encoded = await encoder(f"{mess_id_1}-{mess_id_2}")
            link = f"t.me/{c.me.username}?start=get_{encoded}"
            await m.reply_text(f"Here is your link `{link}`")
            return
        except ValueError:
            await m.reply_text("Invalid link")
            return
        except Exception as e:
            LOGGER.error(e)
            await m.reply_text(e)
            return

@Client.on_message(filters.command("changedb") & bot_owner_filt)
@start_in_private
async def change_my_db_channel(c: Client, m: Message):
    if len(m.command) < 3:
        await m.reply_text(
            "Usage\n/changed [bot id] [new channel id]"
        )
        return
    else:
        try:
            bot = int(m.command[1])
            chat = int(m.command[2])
            channel = await c.get_chat_member(chat, c.me.id)
            if channel.status == CMS.ADMINISTRATOR:
                CLIENTS().update_db_channel(bot, chat)
                await m.reply_text(f"Changed db channel to {chat}\nChange will take effect after restart of the bot")
                return
            else:
                await m.reply_text("Make me admin in the channel first")
                return
        except ValueError:
            await m.reply_text("Bot id and channel id should be integer")
            return
        except:
            await m.reply_text("Make me admin in the channel first")
            return
        