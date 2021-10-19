from gerousiabot import bot_handlers
from unittest.mock import Mock, patch
from enum import Enum
import pytest

Test_Response = Enum('Test_Response', "CHECK_USERS CHECK_DOTA BLANK")


def test_start():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    bot_handlers.start(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Gerousia bot! 🤖")


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


@pytest.mark.parametrize("_input,expected", [(Test_Response.CHECK_USERS, 0),
                                             (Test_Response.BLANK, 0)],
                         ids=["User query", "Other query"])
@patch("gerousiabot.bot_handlers.Response", Test_Response)
def test_keyboard_button_pressed(_input, expected):
    mocked_update, mocked_context = Mock(), Mock()
    mocked_update.effective_chat.id = 0
    mocked_update.callback_query.data = _input

    bot_handlers.keyboard_button_pressed(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    assert mocked_update.effective_chat.id == expected  # Yes, this is lazy. I am open to suggestions


def test_get_user_list():
    names = bot_handlers.get_user_list()
    assert len(names) == 3


def test_format_user_list():
    test_list = [str(x) for x in range(3)]
    test_str = bot_handlers.format_user_list(test_list)
    assert test_str == '- 0\n- 1\n- 2\n'
