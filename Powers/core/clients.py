from platform import python_version
from sys import exit as exiter

from pyrogram import __version__, idle
from pyrogram.raw.all import layer
from pyromod import Client

from Powers import *
from Powers.database import MongoDB
from Powers.database.clients_db import CLIENTS
from Powers.functions.decorators import bot_admin_check
from Powers.functions.supports import *


class FILES(Client):
    """Starts the Pyrogram Client on the Bot Token when we do 'python3 -m Powers'"""

    def __init__(self):
        self.other: list[Client] = []
        self.main_bot: Client = Client(
            "File_Share",
            bot_token=BOT_TOKEN,
            plugins=dict(root="Powers.plugins"),
            api_id=API_ID,
            api_hash=API_HASH,
        )

    async def start(self):
        """Start the bot."""
        LOGGER.info("Starting main bot...")
        await self.main_bot.start()
        await load_support_users(self.main_bot.me.id, SUDO)
        owner = await self.main_bot.get_users(OWNER_ID)
        self.main_bot.is_main = True
        self.main_bot.owner = owner
        try:
            is_admin = await bot_admin_check(self.main_bot, int(DB_CHANNEL))
            if is_admin:
                self.main_bot.db_channel = await self.main_bot.get_chat(int(DB_CHANNEL))
            else:
                LOGGER.info("Make sure I am admin in db channel")
                exiter(1)
        except Exception as e:
            await self.main_bot.send_message(owner.id, f"Your db channel is invalid change it and restart the bot\nBot id: `{self.main_bot.me.id}`\n{e}")
        LOGGER.info(
            f"Pyrogram v{__version__} (Layer - {layer}) started on {self.main_bot.me.username}",
        )
        LOGGER.info(f"Python Version: {python_version()}\n")

    async def start_other(self):
        """Star other bots"""
        LOGGER.info("Starting other bots")
        clients = CLIENTS().get_all_clients()
        for i, j in enumerate(clients):
            if not j:
                continue
            try:
                client = Client(
                    f"FILES#{i+1}",
                    API_ID,
                    API_HASH,
                    bot_token=j['bot_token'],
                    plugins=dict(root="Powers.plugins"),
                )
                await client.start()
                await load_support_users(client.me.id, SUDO)
                try:
                    owner = await client.get_users(int(j['owner_id']))
                except:
                    continue
                try:
                    is_admin = await bot_admin_check(client, j["db_channel"])
                    if not is_admin:
                        await client.send_message(owner.id, "Make sure I am admin in the db channel")
                    client.db_channel = await client.get_chat(int(j['db_channel']))
                except Exception as e:
                    await client.send_message(owner.id, f"Your db channel is invalid change it and restart the bot\nBot id: `{client.me.id}`\n{e}")
                suff = {1: 'st', 2: 'nd', 3: 'rd'}.get(i+1 % 10, 'th')
                CLIENTS().update_bot_id(client.me.id,client.bot_token)
                client.is_main = False
                client.owner = owner
                sudo = get_support_staff(client.me.id)
                LOGGER.info(f"""
STARTED {i+1}{suff} client:
    Owner of this bot: {j['owner_id']}
    sudo users: {', '.join(sudo)}""")
                self.other.append(client)
            except Exception as e:
                LOGGER.error(f"{i+1}: {e}")
                continue
        LOGGER.info(
            f"Successfully started all the client. Current number of clients running: {len(clients)+1}")
    async def stop(self):
        """Stop the bot and send a message to MESSAGE_DUMP telling that the bot has stopped."""
        clients = self.other + [self.main_bot]
        for i in clients:
            await i.send_message(i.owner.id, "I am going offline see ya!")
            await i.stop()
        MongoDB.close()
        LOGGER.info("Bot stopped.")

    async def startup(self):
        await self.start()
        await self.start_other()
        clients = self.other + [self.main_bot]
        for client in clients:
            await client.send_message(client.owner.id, "Your bot is now online")
        await idle()

