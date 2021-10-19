from enum import Enum
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext


Response = Enum('Response', "CHECK_USERS CHECK_DOTA BLANK")


def get_bot_handlers() -> list:
    """
    Gets the list of the handlers to be used by the bot
    :return: the list of the handlers
    """
    start_handler = CommandHandler('start', start)
    user_query_handler = CommandHandler('chkusers', check_users)
    button_handler = CallbackQueryHandler(keyboard_button_pressed)
    unknown_handler = MessageHandler(Filters.command, unknown_command)

    # unknown command handler must be the last added handler or we run into logical errors
    return [start_handler, button_handler, user_query_handler, unknown_handler]


def start_keyboard() -> list:
    """Initialize the keyboard"""
    keyboard = [InlineKeyboardButton("Check Users", callback_data=Response.CHECK_USERS),
                InlineKeyboardButton("Blank button", callback_data=Response.BLANK)]
    return keyboard


def keyboard_button_pressed(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery for keyboard buttons"""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")  # for debugging, remove once final

    if query.data is Response.CHECK_USERS:
        users = format_user_list(get_user_list())
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Users currently on the server:\n" + users)
    elif query.data is Response.BLANK:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing to see here.")
    else:
        print("Nothing happened.")
        return


def get_user_list() -> list:
    """
    Query discord user list.
    Not yet implemented. Returns test data
    """
    user_list = ['rick', 'ash', 'jk']
    return user_list


def format_user_list(user_list: list) -> str:
    """ Returns a formatted user list with one name per line."""
    # new_list = [f"- {x}\n" for x in user_list]
    # Equivalent to below
    new_list = map(lambda x: f"- {x}\n", user_list)
    formed_string: str = ''.join(new_list)

    return formed_string


def start(update, context) -> None:
    """Handler definition for the bot start command: /start"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Gerousia bot! 🤖")
    kb_markup = InlineKeyboardMarkup(start_keyboard())
    update.message.reply_text('Please select one:', reply_markup=kb_markup)


def check_users(update, context) -> None:
    """
    Handler definition for check users command: /chkusers
    Used to retrieve the names of the users currently logged in.
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Users currently on the server:\n" + format_user_list(get_user_list()))


def help_command(update, context) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def unknown_command(update, context) -> None:
    """Handler definition to manage any unknown commands"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
