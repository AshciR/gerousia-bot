from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext


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
    keyboard = [InlineKeyboardButton("Check Users", callback_data='user_check'),
                InlineKeyboardButton("Blank button", callback_data='blank_button')]
    return keyboard


def keyboard_button_pressed(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery for keyboard buttons"""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")  # for debugging, remove once final
    if query.data == "user_check":
        users = format_user_list(get_user_list())
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Users currently on the server:\n" + users)
    elif query.data == "blank_button":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing to see here.")
    else:
        print("Nothing happened.")
        return


def get_user_list() -> list:
    """
    Query discord user list.
    Not yet implemented. Returns test data
    """
    user_list = ['Alrick', 'Richard', 'Jheuvan']
    return user_list


def format_user_list(user_list: list) -> str:
    """ Returns a formatted user list with one name per line."""
    string_layout = str()
    for name in user_list:
        string_layout = string_layout + f"- {name}\n"

    return string_layout


def start(update, context) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Gerousia bot! U+1F916")
    kb_markup = InlineKeyboardMarkup(start_keyboard())
    update.message.reply_text('Please select one:', reply_markup=kb_markup)


def check_users(update, context) -> None:
    """Retrieve user list via command: /chkusers"""
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Users currently on the server:\n" + format_user_list(get_user_list()))


def help_command(update, context) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def unknown_command(update, context) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
