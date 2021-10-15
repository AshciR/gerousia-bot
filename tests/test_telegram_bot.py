from gerousiabot import telegram_bot


def test_say_hello():
    assert 'The Telegram Bot says hello' == telegram_bot.say_hello()
