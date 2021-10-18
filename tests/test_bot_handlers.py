from gerousiabot import bot_handlers
from unittest.mock import Mock
import pytest


def test_start():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    bot_handlers.start(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Gerousia bot! U+1F916")


def test_help_command():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    bot_handlers.help_command(mocked_update, mocked_context)

    mocked_update.message.reply_text.assert_called()
    mocked_update.message.reply_text.assert_called_with("Use /start to test this bot.")


def test_unknown():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    bot_handlers.unknown_command(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Sorry, I didn't understand that command.")


def test_get_bot_handlers():
    handlers = bot_handlers.get_bot_handlers()

    assert len(handlers) == 4


def test_start_keyboard():
    buttons = bot_handlers.start_keyboard()
    assert len(buttons) == 2


@pytest.mark.parametrize("_input,expected", [("user_check", "Users currently on the server:"),
                                             ("blank_button", "Nothing to see here.")],
                         ids=["User query", "Other query"])
def test_keyboard_button_pressed(_input, expected):
    mocked_update, mocked_context, mocked_query = Mock(), Mock(), Mock()
    mocked_update.effective_chat.id = 0
    mocked_update.callback_query.data = _input

    bot_handlers.keyboard_button_pressed(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()


def test_get_user_list():
    names = bot_handlers.get_user_list()
    assert len(names) == 3
