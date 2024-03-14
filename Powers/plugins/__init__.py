main_help_txt = """
**General commands:**
    • /start: Start the bot.
    • /help: To get help menu.
    • /deploymybot: To deploy your own bot

**Bot Owner & Sudo Commands:**
    • /getfilelink: Return encoded file link.
    • /getbatch: Give the file link for the batch.
    • /deletebot: Delete your current bot.
    • /stopmybot: Stop your bot (NOTE: YOU HAVE TO THEN START YOUR BOT FROM MAIN BOT).
    • /startmybot [id of your bot]: Will start your bot.
    • /restart: Will start every bot
    • /addsudo [reply to message]: Will add replied user to sudo
    • /rmsudo [reply to message]: Will remove replied user from sudo
    • /addfsub [channel id] [type]: Add channel in force subscribe. Default to auto
        available types:
            request: User have to request to join the channel for this type of force subscribe
            direct: User will able to directly join the channel.
            auto: If given channel is private it will bw request force sub and if it is public then it will be direct.

**Admin Commands:**
    • /ban [reply to user]: Ban the given user.
    • /tban [time till unban] [reply to user]: Temp ban the user.
    • /unban [reply to user]: Unbans replied user
    • /mute [reply to user]: Mutes the user
    • /unmute [reply to user]: Unmutes replied user
    • /tmute [time till unmute] [reply to user]: Temp mutes the user
    • /kick [reply to user]: Kicks the user

    Note: Tille time should be in format like 1d or 3d where 
        `m` means minutes
        `h` means hours
        `d` means days
"""

other_help_txt = """
**General commands:**
    • /start: Start the bot.
    • /help: To get help menu

**Bot Owner Commands:**
    • /getfilelink: Return encoded file link.
    • /getbatch: Give the file link for the batch.
    • /deletebot: Delete your current bot.
    • /stopmybot: Stop your bot (NOTE: YOU HAVE TO THEN START YOUR BOT FROM MAIN BOT).
    • /startmybot [id of your bot]: Will start your bot.
    • /restart: Will start every bot
    • /addsudo [reply to message]: Will add replied user to sudo
    • /rmsudo [reply to message]: Will remove replied user from sudo
    • /addfsub [channel id] [type]: Add channel in force subscribe. Default to auto
        available types:
            request: User have to request to join the channel for this type of force subscribe
            direct: User will able to directly join the channel.
            auto: If given channel is private it will bw request force sub and if it is public then it will be direct.

**Admin Commands:**
    • /ban [reply to user]: Ban the given user.
    • /tban [time till unban] [reply to user]: Temp ban the user.
    • /unban [reply to user]: Unbans replied user
    • /mute [reply to user]: Mutes the user
    • /unmute [reply to user]: Unmutes replied user
    • /tmute [time till unmute] [reply to user]: Temp mutes the user
    • /kick [reply to user]: Kicks the user
    
    Note: Tille time should be in format like 1d or 3d where 
        `m` means minutes
        `h` means hours
        `d` means days
"""