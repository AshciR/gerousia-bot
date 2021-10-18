"""
This module will hold the functions used for the Telegram Bot.

"""
import logging
import os
import bot_handlers

from dotenv import load_dotenv
from telegram.ext import Updater


def setup_logger() -> object:
    """
    Creates and configures a logger that will log
    to both the console and a file (file.log)
    :rtype: object the configured logger
    """
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('file.log')
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


def get_api_token(key) -> str:
    """
    Gets the API token for a given key
    :param key: the key for the token you want returned
    :return: the API token
    """
    load_dotenv()
    return os.getenv(key)


def configure_bot(api_token, handlers) -> Updater:
    """
    Configures the bot with correct handlers
    :param api_token: the API token
    :param handlers: the handlers to be added to the bot
    :return:
    """
    # Set up the instance of the bot using token from the @BotFather
    bot_updater = Updater(token=api_token)
    bot_dispatcher = bot_updater.dispatcher

    for handler in handlers:
        bot_dispatcher.add_handler(handler)

    return bot_updater


def run_bot():
    bot_token = get_api_token('API_KEY')
    handlers = bot_handlers.get_bot_handlers()
    telegram_bot = configure_bot(api_token=bot_token, handlers=handlers)
    start_bot(telegram_bot)


def start_bot(bot_updater):
    """
    Starts a provided bot
    :param bot_updater:
    """
    # Polls the server for new messages, could replace with webhook later on
    bot_updater.start_polling()
    # Waits for termination signals to stop polling. Locally press Ctrl+C in the console to stop.
    bot_updater.idle()


def say_hello() -> str:
    """Place holder function that simulates the bot saying hello"""
    return 'The Telegram Bot says hello'
