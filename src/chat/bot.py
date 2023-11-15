from telebot import types
from telebot.types import Message
import asyncio
import telebot
import os
import logging
import validators

from src.algorithms.algo import do_search
from src.structures import FilmId
from src.chat.models import *

logger = logging.getLogger(__name__)

logger.info("Running telegram bot.")


bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


def clear_user_films(user: User):
    user.film1 = None
    user.film2 = None
    user.save()

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
    user = User.get_or_none(User.username == msg.from_user.username)
    if user is not None:
        user.delete_instance()
    bot.reply_to(msg, f"До свидания!")


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
def set_film_ru_mode(msg):
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
    user.mode = "film_ru"
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
    modeKBoard = types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=True
    )
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


def _suggest(search_string, mode="ivi") -> List[FilmId]:
    # TODO
    return [
        FilmId("Шрек (Мультфильм 2001)", "https://www.ivi.ru/watch/99983"),
        FilmId("Шрек 2 (Мультфильм 2004)", "https://www.ivi.ru/watch/112470"),
        FilmId("Шрек Третий (Мультфильм 2007)", "https://www.ivi.ru/watch/105738"),
        FilmId("Шрек навсегда (Мультфильм 2010)", "https://www.ivi.ru/watch/105743"),
    ]

def search(user: User):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        return loop.run_until_complete(do_search(FilmId(name='', url=user.film1), FilmId(name='', url=user.film2))) 
    finally:
        loop.close()


@bot.callback_query_handler(func=lambda call: True)
def film_callback(call: types.CallbackQuery):
    user = User.get_or_none(User.username == call.from_user.username)
    if validators.url(call.data):  # Ввели ссылку на фильм
        if user.film1 == None:
            user.film1 = call.data
            user.save()
            bot.send_message(call.message.chat.id, "Выбери второй фильм")
        elif user.film2 == None:
            user.film2 = call.data
            user.save()
            bot.send_message(
                call.message.chat.id, "Ищем фильм\nЭто может занять какое-то время"
            )
            recomends = search(user)
            bot.send_message(call.message.chat.id, f"Предлагаем к просмотру {recomends.recommended_films[0].url}")
            clear_user_films(user)
            
    else:
        bot.send_message(call.message.chat.id, "Произошла проблема")


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
    if validators.url(msg.text):  # Ввели ссылку на фильм
        if user.film1 == None:
            user.film1 = msg.text
            user.save()
            bot.send_message(msg.chat.id, "Выбери второй фильм")
        elif user.film2 == None:
            user.film2 = msg.text
            user.save()
            bot.send_message(msg.chat.id, "Ищем подходящий фильм")
            loop = asyncio.get_event_loop()
            recomends = search(user)
            bot.send_message(msg.chat.id, f"Предлагаем к просмотру {recomends.recommended_films[0].url}")
            clear_user_films(user)
    else:  # Поиск фильма по названию
        suggests = _suggest(msg.text, mode=user.mode)
        filmSuggestKBoard = types.InlineKeyboardMarkup(
            row_width=1,
        )
        for suggest in suggests:
            filmSuggestKBoard.add(
                types.InlineKeyboardButton(text=suggest.name, callback_data=suggest.url)
            )

        bot.send_message(msg.chat.id, "Выберете фильм", reply_markup=filmSuggestKBoard)




if __name__ == "__main__":
    bot.polling(none_stop=True)
