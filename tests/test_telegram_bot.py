from unittest.mock import patch

from src.gerousiabot import telegram_bot
from src.gerousiabot.telegram_bot import TelegramBot


@patch("gerousiabot.telegram_bot.Updater")
@patch("gerousiabot.telegram_bot.DiscordBot")
def test_configure_bot_handlers(mock_discord_bot, mock_updater):
    # Given: We have the Telegram bot setup
    bot = TelegramBot('abc', [], mock_discord_bot)
    mock_handlers = [1, 2, 3]
    mock_updater.return_value.dispatcher = MockDispatcher()

    # When: The bot handlers are configured
    bot.configure_bot_handlers(mock_updater, mock_handlers)

    # Then: The updater should have n method calls
    assert len(mock_updater.method_calls) == 3


@patch("gerousiabot.telegram_bot.Updater")
@patch("gerousiabot.telegram_bot.DiscordBot")
def test_start_bot(mock_discord_bot, mock_updater):
    # Given: We have the Telegram bot setup
    bot = TelegramBot('abc', [], mock_discord_bot)

    # When: The bot is started
    bot.start_bot()

    # Then: The updater should call the start_polling and idle methods
    assert len(bot.telegram_bot_updater.method_calls) == 2
    assert bot.telegram_bot_updater.method_calls[0][0] == 'start_polling'
    assert bot.telegram_bot_updater.method_calls[1][0] == 'idle'


@patch("gerousiabot.utils.get_env_variable", return_value='1234')
@patch("gerousiabot.telegram_bot.DiscordBot")
@patch("gerousiabot.telegram_bot_handlers.get_bot_handlers")
@patch("gerousiabot.telegram_bot.TelegramBot")
def test_run_bot(mock_telegram_bot, mock_get_bot_handlers, mock_discord_bot, mock_get_env_variable):
    # When: The Telegram Bot is ran
    telegram_bot.run_bot(mock_discord_bot)

    # Then: The following methods should be called
    mock_get_env_variable.assert_called()
    mock_get_bot_handlers.assert_called()
    assert mock_telegram_bot.called


class MockDispatcher:
    def add_handler(self, handler):
        return 'Mock {} handler called'.format(handler)
