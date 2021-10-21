from unittest.mock import Mock, patch

from gerousiabot import telegram_bot


@patch("gerousiabot.telegram_bot.os.getenv")
def test_get_api_token(mocked_env):
    mocked_env.return_value = '56gghh123'
    assert '56gghh123' == telegram_bot.get_api_token('TEST_KEY')


def test_say_hello():
    assert 'The Telegram Bot says hello' == telegram_bot.say_hello()


@patch("gerousiabot.telegram_bot.start_bot")
@patch("gerousiabot.telegram_bot.configure_bot_handlers")
@patch("gerousiabot.bot_handlers.get_bot_handlers")
@patch("gerousiabot.telegram_bot.get_api_token")
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


def test_start_bot():
    mocked_bot_updater = Mock()
    telegram_bot.start_bot(mocked_bot_updater)

    mocked_bot_updater.start_polling.assert_called()
    mocked_bot_updater.idle.assert_called()
