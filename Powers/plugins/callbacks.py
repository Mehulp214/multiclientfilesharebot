from pyrogram import Client, ContinuePropagation, filters
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM

from Powers.database.clients_db import CLIENTS
from Powers.database.forcesub_db import FSUBS
from Powers.functions.clients_extra import start_particular, stop_particular
from Powers.functions.kb_helpers import get_yes_no_kb
from Powers.plugins import *
from Powers.plugins.client_add import get_deploy_help
from Powers.plugins.start import what_can_I_do


@Client.on_callback_query(filters.regex(r"^get."))
async def get_type_data(c: Client, q: CallbackQuery):
    data = q.data.split(".", 1)
    message = q.message.reply_to_message if q.message.reply_to_message else q.message
    if data[1] == "deployOwn":
        await get_deploy_help(c, message)
        await q.message.delete()
        return
    elif data[1] == "help":
        await what_can_I_do(c, message)
        await q.message.delete()
        return
    elif data[1] == "main":
        user = q.from_user
        await q.edit_message_text(
            f"Hi {user.mention if user else q.message.chat.title}!\nMy self {c.me.first_name}\nI am a file sharer bot with some basic admin commands.\n**Want to deploy your own bot like me?**\nJust type `/deployown` to know how you can do so."
        )
    elif data[1] == 'cancel':
        await q.answer('Cancelled', True)
        await q.message.delete()



@Client.on_callback_query(filters.regex(r"^yes_"))
async def yes_no_callbacks(c: Client, q: CallbackQuery):
    data = q.data.split("_")

    if data[0] == "yes":
        fsub = FSUBS()
        if data[1] == "change":
            await q.answer("Changing fsub type...")
            c_id = int(data[-1])
            type_ = data[-2]
            fsub.update_fsub_type(c_id, type_, c.me.id)
            await q.edit_message_text(f"Changed fsub type to {type_} of chat {c_id}")
            return
        else:
            await q.answer("Removing chat from force subs")
            c_id = int(data[-1])
            fsub.remove_fsub(c_id)
            await q.edit_message_text(f"Removed {c_id} from force subscribe")
            return

    else:
        raise ContinuePropagation

@Client.on_callback_query(filters.regex(r"^(delete:|delete_all:|stop:|stop_all:|yes:|no:|start:)"))
async def bot_related_datas(_, q: CallbackQuery):
    data = q.data.split(":", 1)
    to_do = data[0]
    if to_do in ['yes', 'no']:
        data = data[1].split(':', 1)
        cl = data[1]
        to_do = data[0]
        if to_do == 'delete':
            CLIENTS().remove_cliet(int(cl))
            await q.answer('Deleted your bot')
            try:
                await stop_particular(int(cl))
            except Exception as e:
                await q.edit_message_text(e)
                return
            await q.edit_message_text('Removed your client and stopped it')
            return
        elif to_do == 'stop':
            await q.answer('Trying to stop your bot')
            try:
                await stop_particular(int(cl))
            except Exception as e:
                await q.edit_message_text(e)
                return
            await q.edit_message_text('Deleted your client and stopped it')
            return
        elif to_do == 'delete_all':
            clientss = CLIENTS().get_clients_by_id(int(cl))
            for i in clientss:
                CLIENTS().remove_cliet(i['bot_id'])
                try:
                    await stop_particular(int(i['bot_id']))
                except:
                    continue
            await q.edit_message_text('Removed all of your clients and stopped them')
            return
        elif to_do == 'stop_all':
            for i in clientss:
                CLIENTS().remove_cliet(i['bot_id'])
                try:
                    await stop_particular(int(i['bot_id']))
                except:
                    continue
            await q.edit_message_text('Stopped all of your clients')
            return
    elif to_do == 'start':
        client = data[1]
        await start_particular(int(client))
        return
    else:
        kb = await get_yes_no_kb(q.data)
        await q.edit_message_text(f"Are you sure you want to do this?", reply_markup=kb)
        return
