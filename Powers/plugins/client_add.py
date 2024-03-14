from pyrogram import filters, idle
from pyrogram.types import Message
from pyromod import Client
from pyromod.exceptions import ListenerTimeout

from Powers import LOGGER
from Powers.core import app
from Powers.database.clients_db import CLIENTS
from Powers.functions.decorators import bot_owner_filt, start_in_private
from Powers.vars import API_HASH, API_ID


@Client.on_message(filters.command("deployown"))
@start_in_private
async def get_deploy_help(c: Client, m: Message):
    txt = "You want to deploy your own bot??\nJust type /deploymybot to deploy one of your own\nNote: Only bot owner and sudoers can deploybots"
    await m.reply_text(txt)
    return


@Client.on_message(filters.command("deploymybot") & bot_owner_filt)
@start_in_private
async def deploying_my_own(c: Client, m: Message):
    if not c.is_main:
        await m.reply_text(
            f"Do this in main bot i.e. {app.main_bot.me.username} here"
        )
        return

    else:
        user_id = m.from_user.id
        c_id = m.chat.id
        while True:
            try:
                response = await c.ask(c_id, "Ok you give me your bot token\nType /cancel to stop making your bot", filters.text, timeout=120)
            except ListenerTimeout:
                await m.reply_text("You took too long to respond")
                return
            if response.text == "/cancel":
                await m.reply_text("Stopped the current process")
                return
            else:
                try:
                    int(response.text.split(":")[0])
                    bot_token = response.text
                    break
                except ValueError:
                    await m.reply_text("Invalid bot token give me valid one")
                    await response.delete()

        while True:
            try:
                response = await c.ask(c_id, "Now give me db channel id where you will store your files\nMake sure your bot is admin there\nType /cancel to stop ", filters.text, timeout=120)
            except ListenerTimeout:
                await m.reply_text("You took too long to respond")
                return
            if response.text == "/cancel":
                await m.reply_text("Stopped the current process")
                return

            try:
                chat_id = int(response.text)
                break
            except ValueError:
                await m.reply_text("Give me channel id please")
                await response.delete()

        CLIENTS().load_client(bot_token, user_id, int(chat_id))
        total = len(app.other)
        to_edit = await m.reply_text("Successfully added your client\nTrying to start your bot")
        client = Client(
            f"FILES#{total+1}",
            API_ID,
            API_HASH,
            bot_token=bot_token,
            plugins=dict(root="Powers.plugins")
        )

        try:
            await client.start()
            CLIENTS().update_bot_id(client.me.id, bot_token)
            try:
                client.db_channel = await client.get_chat(int(chat_id))
            except:
                await m.reply_text(f"Invalid db channel make sure I am admin there\nUpdate it later\nBot id: `{client.me.id}`")
            client.owner = await client.get_users(user_id)
            client.is_main = False
            app.other.append(client)
            await to_edit.edit_text("Successfully started your bot")
            await idle()
            LOGGER.info("Added a new client")
        except Exception as e:
            await to_edit.edit_text(f"Error\n{e}")
            await m.reply_text("Report this error the the owner and ask him to restart whole bot")
            return
