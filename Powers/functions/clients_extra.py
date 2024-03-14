from pyrogram import idle
from pyromod import Client

from Powers import *
from Powers.core import app
from Powers.database.clients_db import CLIENTS
from Powers.functions.supports import *


async def start_particular(bot_id):
    """Start a particular client"""
    LOGGER.info("Starting client")
    try:
        client = CLIENTS().get_client_info(bot_id)
        clients = len(CLIENTS().get_all_clients())
        client = Client(
            f"FILES#{clients+1}",
            API_ID,
            API_HASH,
            bot_token=client['bot_token'],
            plugins=dict(root="Powers.plugins"),
        )
        await client.start()
        owner = await client.get_users(int(client['owner_id']))
        try:
            client.db_channel = await client.get_chat(int(client['db_channel']))
        except Exception as e:
            await client.send_message(owner.id, f"Your db channel is invalid change it and restart the bot\nBot id: `{client.me.id}`\n{e}")
        await load_support_users(app.main_bot.me.id, SUDO)
        client.is_main = False
        client.owner = owner
        app.other.append(client)
        LOGGER.info("Successfully started the client")
        await client.send_message(owner.id, "Your bot is now online!")
        await idle()
    except Exception as e:
        LOGGER.error(f"Start particular: {e}")

async def stop_particular(bot_id):
    try:
        for i in app.other:
            if bot_id == i.me.id:
                await i.send_message(i.owner.id, f"I am going off byee\nMy id: {i.me.id}")
                await i.stop()
                return
        return
    except Exception as e:
        LOGGER.error(f"Stop particular: {e}")