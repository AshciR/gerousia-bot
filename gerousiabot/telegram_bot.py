"""
This module will hold the functions used for the Telegram Bot.

"""

from typing import List

from telegram.ext import Updater, Handler

from gerousiabot import telegram_bot_handlers
from gerousiabot import utils
from gerousiabot.discord_bot import DiscordBot

logger = utils.setup_logger()


class TelegramBot:
    """
       Configures the bot with supplied handlers
       :param api_token: the API token
       :param handlers: the handlers to be added to the bot
       :param discord_bot: the DiscordBot that the Telegram bot uses
       :return: the instance of the TelegramBot
       """

    def __init__(self,
                 api_token: str,
                 handlers: List[Handler],
                 discord_bot: DiscordBot):
        logger.debug('Creating TelegramBot with with valid token {}'.format(api_token is not None))
        # Set up the instance of the bot using token from the @BotFather
        self.telegram_bot_updater = Updater(token=api_token)
        self.configure_bot_handlers(self.telegram_bot_updater, handlers)

        self.discord_bot = discord_bot

    def configure_bot_handlers(self, telegram_bot_updater: Updater, handlers: List[Handler]) -> Updater:
        """
        Attaches the provided handlers to the provided Telegram bot
        :param telegram_bot_updater: the updater that the handlers will be attached to
        :param handlers: the handlers for bot
        :return: the configured Updater
        """

        bot_dispatcher = telegram_bot_updater.dispatcher

        for handler in handlers:
            bot_dispatcher.add_handler(handler)

        return telegram_bot_updater

    def start_bot(self):
        """
        Starts the TelegramBot
        """
        # TODO: We might have to make these run as co-routines
        # Polls the server for new messages, could replace with webhook later on
        self.telegram_bot_updater.start_polling()
        # Waits for termination signals to stop polling. Locally press Ctrl+C in the console to stop.
        self.telegram_bot_updater.idle()


def run_bot(discord_bot: DiscordBot):
    bot_token = utils.get_env_variable('API_KEY')
    handlers = telegram_bot_handlers.get_bot_handlers()
    telegram_bot = TelegramBot(bot_token, handlers, discord_bot)

    telegram_bot.start_bot()
