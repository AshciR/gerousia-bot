from gerousiabot import telegram_bot
from unittest.mock import Mock,patch


def test_start():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    telegram_bot.start(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="I'm a bot, please talk to me!")

def test_echo():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0
    mocked_update.message.text = "test message"

    telegram_bot.echo(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="test message")

def test_unknown():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    telegram_bot.unknown(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Sorry, I didn't understand that command.")

@patch("gerousiabot.telegram_bot.os.getenv")
def test_get_api_token(mocked_env):
    mocked_env.return_value = '56gghh123'
    assert '56gghh123'==telegram_bot.get_api_token('TEST_KEY')

def test_say_hello():
    assert 'The Telegram Bot says hello' == telegram_bot.say_hello()

@patch("gerousiabot.telegram_bot.start_bot")
@patch("gerousiabot.telegram_bot.configure_bot")
@patch("gerousiabot.telegram_bot.get_bot_handlers")
@patch("gerousiabot.telegram_bot.get_api_token")
def test_run_bot(mocked_get_api_token,mocked_get_bot_handlers,mocked_configure_bot,mocked_start_bot):
    telegram_bot.run_bot()

    mocked_get_api_token.assert_called()
    mocked_get_bot_handlers.assert_called()
    mocked_configure_bot.assert_called()
    mocked_start_bot.assert_called()

@patch("gerousiabot.telegram_bot.logging")
def test_setup_logger(mocked_logging):
    telegram_bot.setup_logger()

    mocked_logging.getLogger.assert_called()
    mocked_logging.StreamHandler.assert_called()
    mocked_logging.FileHandler.assert_called()

    mocked_logging.StreamHandler().setLevel.assert_called()
    mocked_logging.FileHandler().setLevel.assert_called()

    assert mocked_logging.Formatter.call_count == 2

    mocked_logging.StreamHandler().setFormatter.assert_called()
    mocked_logging.FileHandler().setFormatter.assert_called()

    assert mocked_logging.getLogger().addHandler.call_count == 2

def test_get_bot_handlers():
    handlers = telegram_bot.get_bot_handlers()

    assert 3 == len(handlers)

@patch("gerousiabot.telegram_bot.Updater")
def test_configure_bot(mocked_updater):
    mocked_config = Mock()
    handler = Mock()
    mocked_updater.return_value = mocked_config

    telegram_bot.configure_bot('test', [handler])

    mocked_config.dispatcher.add_handler.assert_called()

def test_start_bot():
    mocked_bot_updater = Mock()
    telegram_bot.start_bot(mocked_bot_updater)

    mocked_bot_updater.start_polling.assert_called()
    mocked_bot_updater.idle.assert_called()

