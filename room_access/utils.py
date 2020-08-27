import json
import logging
from typing import Tuple, List

from telebot.types import Message

from room_access.app import bot
from room_access.services.admin_sevice import check_admin_exist_by_username


def admin_required(controller):
    """Декоратор. Проверка на то, что сообщение от администратора"""
    def wrapper(message: Message):
        admin_username = message.from_user.username
        if check_admin_exist_by_username(admin_username):
            return controller(message)
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='❌ Вы не являетесь администратором, доступ запрещен!'
            )
    return wrapper


# Не закончено
def logger(func):
    """Декоратор. Ловит все исключения, логирует их и опять выбрасывает исключение."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e


def prepare_command_args(message_text: str) -> tuple:
    """Принимает строку, содержащую текст сообщения c командой,
    возвращает кортеж со всеми аргументами, разделенными пробелами"""
    words: List[str] = message_text.split(' ')
    words.pop(0)

    args = []
    for word in words:
        try:
            args.append(int(word))
        except ValueError:
            args.append(word)
    return tuple(args)
