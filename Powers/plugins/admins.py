from pyrogram import Client, filters

from Powers.functions.admin_actions import *
from Powers.functions.decorators import restrict_filter


@Client.on_message(filters.command(["ban", "tban", "unban"]) & restrict_filter)
async def ban_unban_userss(c: Client, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to an user to ban them")
        return
    elif m.reply_to_message and not m.reply_to_message.from_user:
        await m.reply_text("Reply to an user to ban them")
        return

    if m.command[0] == "ban":
        await ban_user(c, m)
        return
    elif m.command[0] == "tban":
        await ban_user(c, m, m.command[1])
        return
    elif m.command[0] == "unban":
        await unrestrict_user(m)
        return


@Client.on_message(filters.command(["mute", "tmute", "unmute"]) & restrict_filter)
async def mute_unmute_userss(c: Client, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to an user to mute them")
        return
    elif m.reply_to_message and not m.reply_to_message.from_user:
        await m.reply_text("Reply to an user to mute them")
        return

    if m.command[0] == "mute":
        await mute_user(c, m)
        return
    elif m.command[0] == "tmute":
        await mute_user(c, m, m.command[1])
    elif m.command[0] == "unmute":
        await unrestrict_user(m)
        return


@Client.on_message(filters.command("kick") & restrict_filter)
async def kick_the_user(c: Client, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to an user to kick them")
        return
    elif m.reply_to_message and not m.reply_to_message.from_user:
        await m.reply_text("Reply to an user to kick them")
        return

    await kick_user(c, m)
    return
