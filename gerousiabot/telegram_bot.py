"""
This module will hold the functions used for the Telegram Bot.

"""
from dotenv import load_dotenv
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# basic logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# read API token from file
load_dotenv()
API_KEY = os.getenv('API_KEY')


# Set up the instance of the bot using token from the @BotFather
bot_updater = Updater(token=API_KEY)
bot_dispatcher = bot_updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
unknown_handler = MessageHandler(Filters.command, unknown)

bot_dispatcher.add_handler(start_handler)
bot_dispatcher.add_handler(echo_handler)
bot_dispatcher.add_handler(unknown_handler)

bot_updater.start_polling()  # polls the server for new messages, could replace with webhook later on
"""
Waits for termination signals to stop polling. Locally press Ctrl+C in the console to stop.
"""
bot_updater.idle()


def say_hello() -> str:
    """Place holder function that simulates the bot saying hello"""
    return 'The Telegram Bot says hello'
