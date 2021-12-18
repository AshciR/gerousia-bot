from unittest.mock import Mock, patch

from gerousiabot import telegram_bot
from gerousiabot.telegram_bot import TelegramBot


class MockDispatcher:
    def add_handler(self, handler):
        return 'Mock {} handler called'.format(handler)


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



@patch("gerousiabot.telegram_bot.start_bot")
@patch("gerousiabot.telegram_bot.configure_bot_handlers")
@patch("gerousiabot.bot_handlers.get_bot_handlers")
@patch("gerousiabot.utils.get_env_variable")
def test_run_bot(mocked_get_api_token, mocked_get_bot_handlers, mocked_configure_bot, mocked_start_bot):
    telegram_bot.run_bot()

    mocked_get_api_token.assert_called()
    mocked_get_bot_handlers.assert_called()
    mocked_configure_bot.assert_called()
    mocked_start_bot.assert_called()


@patch("gerousiabot.telegram_bot.Updater")
def test_configure_bot(mocked_updater):
    mocked_config = Mock()
    handler = Mock()
    mocked_updater.return_value = mocked_config

    telegram_bot.configure_bot_handlers('test', [handler])

    mocked_config.dispatcher.add_handler.assert_called()

# def test_start_bot():
#     mocked_bot_updater = Mock()
#     telegram_bot.start_bot(mocked_bot_updater)
#
#     mocked_bot_updater.start_polling.assert_called()
#     mocked_bot_updater.idle.assert_called()
