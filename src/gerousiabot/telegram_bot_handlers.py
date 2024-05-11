from enum import Enum
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

from src.gerousiabot.utils import setup_logger

Response = Enum('Response', ['CHECK_USERS', 'CHECK_DOTA', 'BLANK'])

logger = setup_logger()


def get_bot_handlers() -> list:
    """
    Gets the list of the handlers to be used by the bot
    :return: the list of the handlers
    """
    start_handler = CommandHandler('start', start_command)
    check_users_handler = CommandHandler('chkusers', check_users_command)
    help_handler = CommandHandler('help', help_command)

    button_handler = CallbackQueryHandler(keyboard_button_pressed)
    unknown_handler = MessageHandler(Filters.command, unknown_command)

    # unknown command handler must be the last added handler or we run into logical errors
    return [start_handler, check_users_handler, help_handler, button_handler, unknown_handler]


def start_command(update, context) -> None:
    """Handler definition for the bot start command: /start"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Gerousia bot! 🤖")
    kb_markup = InlineKeyboardMarkup(get_keyboard())
    update.message.reply_text('Please select one:', reply_markup=kb_markup)


def get_keyboard() -> list:
    """Initialize the keyboard"""
    keyboard = [[
        InlineKeyboardButton("Check Users", callback_data=Response.CHECK_USERS.name),
        InlineKeyboardButton("Blank button", callback_data=Response.BLANK.name)
    ]]
    return keyboard


def keyboard_button_pressed(update: Update, context: CallbackContext) -> Optional[Message]:
    """Parses the CallbackQuery for keyboard buttons"""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    logger.debug(f"User Id: {update.effective_user.id} Selected option: {query.data}")
    query.edit_message_text(text=f"You selected selected option: {query.data}")  # for debugging, remove once final

    if query.data == Response.CHECK_USERS.name:
        users = format_user_list(get_user_list())
        return context.bot.send_message(chat_id=update.effective_chat.id,
                                        text=f"Users currently on the server:\n" + users)

    elif query.data == Response.BLANK.name:
        return context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing to see here.")

    else:
        msg = 'A unspecified button was selected'
        logger.error(msg)
        raise RuntimeError(msg)


def get_user_list() -> list:
    """
    Query discord user list.
    Not yet implemented. Returns test data
    """
    user_list = ['rick', 'ash', 'jk']
    return user_list


def check_users_command(update, context) -> None:
    """
    Handler definition for check users command: /chkusers
    Used to retrieve the names of the users currently logged in.
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Users currently on the server:\n" + format_user_list(get_user_list()))


def format_user_list(user_list: list) -> str:
    """ Returns a formatted user list with one name per line."""
    # new_list = [f"- {x}\n" for x in user_list]
    # Equivalent to below
    new_list = map(lambda x: f"- {x}\n", user_list)
    formed_string: str = ''.join(new_list)

    return formed_string


def help_command(update, context) -> None:
    """Displays info on how to use the bot."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Use /start to test this bot.")


def unknown_command(update, context) -> None:
    """Handler definition to manage any unknown commands"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
