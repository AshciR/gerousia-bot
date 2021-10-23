import discord_apis
import telegram_bot

"""
The main function for the bot. 
The supporting code will be called from
the supporting modules.
"""

if __name__ == "__main__":
    print(telegram_bot.say_hello())
    server_status = discord_apis.ping_server()
    print(f"The server returned {server_status}")

    discord_apis.print_user()
    telegram_bot.run_bot()
