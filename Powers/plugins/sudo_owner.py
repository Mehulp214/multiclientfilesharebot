from os import execvp
from sys import executable

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from Powers import LOGFILE, LOGGER
from Powers.core import app
from Powers.database.clients_db import CLIENTS
from Powers.database.forcesub_db import FSUBS
from Powers.database.support_db import SUPPORTS
from Powers.functions.decorators import bot_owner_filt, start_in_private
from Powers.functions.encode_decode import encoder
from Powers.functions.kb_helpers import get_yes_no_kb2, orgainzed_kb
from Powers.functions.load_fsub import get_channels


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

@Client.on_message(filters.command("addfsub") & bot_owner_filt)
async def add_this_to_fsub(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text("Do /devcmd to see how to use this command")
        return

    if len(m.command) == 2:
        try:
            chat_id = int(m.command[1])
            f_type = "auto"
        except ValueError:
            await m.reply_text("Channel id should be integer")
            return

    else:
        try:
            chat_id = int(m.command[1])
            f_type = m.command[2].lower() if m.command[2] in [
                "audo", "direct", "request"] else "auto"
        except ValueError:
            await m.reply_text("Channel id should be integer")
            return

    if f_type == "auto":
        try:
            chat = await c.get_chat(chat_id)
            if chat.username:
                f_type = "direct"
            else:
                f_type = "request"
        except Exception as e:
            await m.reply_text(f"Make user I am admin in {chat_id}")
            LOGGER.error(e)
            return

    try:
        bot_status = (await c.get_chat_member(chat_id, c.me.id)).status
        if bot_status != CMS.ADMINISTRATOR:
            await m.reply_text(f"Make user I am admin in {chat_id}")
            return
    except Exception as e:
        await m.reply_text(f"Make user I am admin in {chat_id}")
        LOGGER.error(e)
        return

    fsub = FSUBS()
    fsub.inser_fsub(chat_id, c.me.id, f_type)

    await m.reply_text(f"Added {chat_id} to force subscribe with {f_type} type")
    return


@Client.on_message(filters.command("rmfsub") & bot_owner_filt)
async def remove_dis_fsub(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text("Do /devcmd to see how to use this command")
        return

    try:
        chat_id = int(m.command[1])
    except ValueError:
        await m.reply_text("Channel id should be integer")
        return

    try:
        chat = await c.get_chat(chat_id)
    except Exception as e:
        await m.reply_text("Looks like I am not part of this chat")
        LOGGER.error(e)
        return

    type_ = FSUBS().inser_fsub(chat_id, c.me.id)
    if type(type_) == bool:
        await m.reply_text("This chat is not in my force subscribe list")
        return

    kb = get_yes_no_kb2(f"rm_{chat_id}")
    txt = f"""
Are you sure you want to remove {chat.title} from force subscribe db?
**Chat info:**
Chat id: {chat_id}
Fsub type = {type_}
Chat type = {str(chat.type).split(".")[1].capitalize()}
"""
    await m.reply_text(txt, reply_markup=kb)
    return


@Client.on_message(filters.command("changetype") & bot_owner_filt)
async def change_fsub_type(c: Client, m: Message):
    if len(m.command) < 3:
        await m.reply_text("Do /devcmd to see how to use this command")
        return

    try:
        chat_id = int(m.command[1])
        f_type = m.command[2].lower()
        if f_type not in ["request", "direct"]:
            await m.reply_text("New force sub type should be request or direct")
            return
    except ValueError:
        await m.reply_text("Channel id should be integer")
        return

    type_ = FSUBS().inser_fsub(chat_id, c.me.id)
    if type(type_) == bool:
        await m.reply_text("This chat is not in my force subscribe list")
        return

    txt = f"Are you sure you want to change force subscribe type from {type_} to {f_type}?"
    kb = get_yes_no_kb2(f"change_{f_type}_{chat_id}")

    await m.reply_text(txt, reply_markup=kb)


@Client.on_message(filters.command("getfsubs") & bot_owner_filt)
async def get_all_fsub_channels(c: Client, m: Message):
    all_f_sub = get_channels(c.me.id)
    txt = "**All force subscribe channel are:**\n\n"
    for one in all_f_sub:
        chat_id = one['c_id']
        try:
            chat = await c.get_chat(chat_id)
            txt += f"Chat name: {chat.title}:\n\tChat id: `{chat.id}`\n\tFsub type: {str(one['type']).capitalize()}\n\n"
        except:
            txt += f"Chat id: `{chat.id}`\n\tFsub type: {str(one['type']).capitalize()}\n\n"
    await m.reply_text(txt)


@Client.on_message(filters.command("logs") & bot_owner_filt)
async def give_me_logs(c: Client, m: Message):
    to_del = await m.reply_text("Genrating logs...")
    with open(LOGFILE) as f:
        raw = ((f.read()))[1]
    await m.reply_document(
        document=LOGFILE,
        quote=True,
    )
    await to_del.delete()
    return