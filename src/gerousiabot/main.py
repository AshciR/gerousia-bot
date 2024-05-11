import discord_bot
# import telegram_bot
from src.gerousiabot import utils

"""
The main function for the bot. 
The supporting code will be called from
the supporting modules.
"""

logger = utils.setup_logger()

if __name__ == '__main__':
    discord_bot_start_msg = 'The Gerousia bot was started'
    logger.info(discord_bot_start_msg)
    print(discord_bot_start_msg)

    discord_bot = discord_bot.run_bot()
    # telegram_bot.run_bot(discord_bot)
