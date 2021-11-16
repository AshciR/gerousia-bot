import telegram_bot
import discord_bot 

"""
The main function for the bot. 
The supporting code will be called from
the supporting modules.
"""

if __name__ == '__main__':
    print(telegram_bot.say_hello())

    discord_bot.run_bot()
    telegram_bot.run_bot()
