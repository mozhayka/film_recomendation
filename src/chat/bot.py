from telebot import types
from telebot.types import Message
import telebot
import os
import logging
import validators
from models import *

logger = logging.getLogger(__name__)

logger.info("Running telegram bot.")


bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


@bot.message_handler(commands=["ping"])
def handle_ping_message(msg: Message):
    logger.info(
        f"ping from {msg.from_user.username}",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )

    bot.reply_to(msg, "pong")


@bot.message_handler(commands=["start"])
def handle_start_message(msg: Message):
    logger.info(
        f"New user {msg.from_user.username}",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )
    if User.get_or_none(User.username == msg.from_user.username) is None:
        User.insert(username=msg.from_user.username, chat_id=msg.chat.id).execute()

    bot.reply_to(msg, f"Привет, {msg.from_user.username}!")

@bot.message_handler(commands=["stop"])
def handle_start_message(msg: Message):
    logger.info(
        f"Stop user {msg.from_user.username}",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )
    if User.get_or_none(User.username == msg.from_user.username) is None:
        User.insert(username=msg.from_user.username, chat_id=msg.chat.id).execute()

    bot.reply_to(msg, f"Привет, {msg.from_user.username}!")



@bot.message_handler(func=lambda msg: msg.text == "IVI")
def set_ivi_mode(msg):
    logger.info(
        f"User {msg.from_user.username} setting mode IVI",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )
    user = User.get_or_none(User.username == msg.from_user.username)
    if user is None:
        bot.reply_to(msg, "Начни с команды /start.")
        return
    user.mode = "ivi"
    user.save()


@bot.message_handler(func=lambda msg: msg.text == "Film.ru")
def set_filmru_mode(msg):
    logger.info(
        f"User {msg.from_user.username} setting mode filomoteka",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )
    user = User.get_or_none(User.username == msg.from_user.username)
    if user is None:
        bot.reply_to(msg, "Начни с команды /start.")
        return
    user.mode = "film.ru"
    user.save()


@bot.message_handler(commands=["mode"])
def handle_mode_message(msg: Message):
    logger.info(
        f"User {msg.from_user.username} setting mode",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )
    user = User.get_or_none(User.username == msg.from_user.username)
    if user is None:
        bot.reply_to(msg, "Твой контекст не найден. Начни с команды /start.")
        return
    modeKBoard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    ivi = types.KeyboardButton(text="IVI")
    filmru = types.KeyboardButton(text="Film.ru")
    modeKBoard.add(ivi, filmru)
    bot.send_message(msg.chat.id, "Выберите режим работы", reply_markup=modeKBoard)


@bot.message_handler(commands=["context"])
def handle_context_message(msg: Message):
    logger.info(
        f"User {msg.from_user.username} show context",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )
    user = User.get_or_none(User.username == msg.from_user.username)
    if user is None:
        bot.reply_to(msg, "Твой контекст не найден. Начни с команды /start.")
        return
    bot.send_message(
        msg.chat.id,
        f"Mode: {user.mode}\nПевый фильм: {user.film1 or 'Не выбран'}\nВторой фильм: {user.film2 or 'Не выбран'}",
    )


@bot.message_handler(commands=["help"])
def handle_help_message(msg: Message):
    logger.info(
        f"help for {msg.from_user.username}",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )

    bot.reply_to(msg, "I need some body!")



@bot.message_handler(func=lambda msg: True)
def hendle_plain_text(msg):
    logger.info(
        f"User {msg.from_user.username} plain text.",
        extra={
            "chat_id": msg.chat.id,
            "username": msg.from_user.username,
            "text": msg.text,
        },
    )
    user = User.get_or_none(User.username == msg.from_user.username)
    if user is None:
        bot.reply_to(msg, "Начни с команды /start.")
        return 
    if validators.url(msg.text): # Ввели ссылку на фильм
        if user.film1==None:
            user.film1=msg.text
            user.save()
            bot.send_message(msg.chat.id, "Выбери второй фильм")
        elif user.film2==None:
            user.film2=msg.text
            user.save()
            bot.send_message(msg.chat.id, "Ищем подходящий фильм")

        else:
            # Предыдущий запрос в обработке
            bot.send_message(msg.chat.id, "Ищем подходящий фильм")
            pass
    else:
        pass


def send_recommendation():
    pass

if __name__ == "__main__":
    bot.polling(none_stop=True)
