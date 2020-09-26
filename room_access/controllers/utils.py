import re
from typing import List

from telebot.types import Message

from room_access.repositories import admin_repository
from room_access.app import bot


def admin_required(controller):
    """
    Декоратор обработчиков сообщений бота.
    Выполняет обернутый обработчик только если пользователь, отпрвивший сообщение, входит в список администраторов.
    """
    def wrapper(message: Message):
        admin_username = message.from_user.username
        if admin_repository.admin_exist_by_username(admin_username):
            return controller(message)
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='❌ Вы не являетесь администратором, доступ запрещен!'
            )
    return wrapper


def command_args_validation(pattern: str, mismatch_answer_text: str, **kwargs):
    """
    Фабрика декораторов.
    Создает декоратор, проверяющий аргумент message на полное совпадение с шаблоном регулярных выражений pattern.
    Если произошло несовпадение, будет отправлено ответное сообщение с текстом mismatch_answer_text
    (принимает остальные аргументы метода .send_message() как **kwargs).
    """
    def command_validation_decorator(controller_func):
        def command_controller_wrapper(message: Message):
            if re.fullmatch(pattern, message.text):
                return controller_func(message)
            else:
                bot.reply_to(message, mismatch_answer_text, **kwargs)
        return command_controller_wrapper
    return command_validation_decorator


def bot_command_controller(command_pattern: str, args_pattern: str,
                           mismatch_answer_text: str, **mismatch_answer_kwargs):
    """
    Фабрика декораторов.
    Создает декоратор, оборачивающий функцию в обработчик сообщений-команд телеграм бота.
    command_pattern - регулярное выражение для проверки команды,
    args_patter - регулярное выражение для проверки аргументов команды

    """
    pass