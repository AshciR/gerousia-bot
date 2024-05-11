from unittest.mock import Mock, patch

import pytest

from src.gerousiabot import telegram_bot_handlers

test_response = telegram_bot_handlers.Response


def test_response_enum():
    assert len(test_response) == 3


def test_start():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    telegram_bot_handlers.start_command(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Gerousia bot! 🤖")


def test_help_command():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    telegram_bot_handlers.help_command(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Use /start to test this bot.")


def test_check_users_command():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    telegram_bot_handlers.check_users_command(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    expected_text = f"Users currently on the server:\n" + telegram_bot_handlers.format_user_list(
        telegram_bot_handlers.get_user_list())
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text=expected_text)


def test_unknown():
    mocked_update = Mock()
    mocked_context = Mock()

    mocked_update.effective_chat.id = 0

    telegram_bot_handlers.unknown_command(mocked_update, mocked_context)

    mocked_context.bot.send_message.assert_called()
    mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Sorry, I didn't understand that command.")


def test_get_bot_handlers():
    handlers = telegram_bot_handlers.get_bot_handlers()

    assert len(handlers) == 5


def test_start_keyboard():
    keyboard = telegram_bot_handlers.get_keyboard()
    assert len(keyboard) == 1
    assert len(keyboard[0]) == 2
    assert isinstance(keyboard, list)


@pytest.mark.parametrize(
    "_input", [test_response.CHECK_USERS.name, test_response.BLANK.name],
    ids=["Check User Button Press", "Blank Button Press"]
)
@patch("gerousiabot.telegram_bot_handlers.Response", test_response)
def test_valid_keyboard_button_pressed(_input):
    mocked_update, mocked_context = Mock(), Mock()

    mocked_update.effective_chat.id = 0
    mocked_update.callback_query.data = _input

    telegram_bot_handlers.keyboard_button_pressed(mocked_update, mocked_context)

    assert mocked_update.effective_chat.id == 0
    mocked_context.bot.send_message.assert_called()


def test_invalid_keyboard_button_throws_exception():
    mocked_update, mocked_context = Mock(), Mock()

    mocked_update.effective_chat.id = 0
    mocked_update.callback_query.data = 'INVALID_BUTTON'

    with pytest.raises(RuntimeError):
        telegram_bot_handlers.keyboard_button_pressed(mocked_update, mocked_context)


def test_get_user_list():
    names = telegram_bot_handlers.get_user_list()
    assert len(names) == 3


def test_format_user_list():
    test_list = [str(x) for x in range(3)]
    test_str = telegram_bot_handlers.format_user_list(test_list)
    assert test_str == '- 0\n- 1\n- 2\n'
