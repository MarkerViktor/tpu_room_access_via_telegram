import re
from typing import Tuple

from telebot import types

from room_access.app import bot
from room_access.services import user_service, exceptions
from room_access.controllers.utils import admin_required


@bot.message_handler(commands=['users_list'])
@admin_required
def users_list(message: types.Message):
    """Отвечает сообщением со списком всех пользователей и их ID"""
    users: Tuple[user_service.UserInfo] = user_service.get_all_users()

    answer_string = f"*Всего пользователей — {len(users)}:*\n" \
                    "`\{user\_id\} : \{last\_name\} \{first\_name\}`\n"

    for user in users:
        answer_string += f'{user.id} : {user.last_name} {user.first_name}\n'

    bot.send_message(chat_id=message.chat.id, text=answer_string, parse_mode='MarkdownV2')


@bot.message_handler(commands=['new_user'])
@admin_required
def new_user(message: types.Message):
    """Создает нового пользователя с указанными фамилией и именем"""

    # Имя или фамилия дожны начинаться с заглавной буквы,
    # содержать только кирилицу, иметь максимальную длину - 75 символов.
    # Пример команды: /new_user Маркер Виктор
    if not re.fullmatch(r'^/new_user [А-Я][а-я]{0,74} [А-Я][а-я]{0,74}$', message.text):
        bot.reply_to(message,
                     text='*Неверная команда\!*\n`\/new\_user \{first\_name\} \{last\_name\}`\n'
                          'Имя или фамилия нового пользователя дожны\n'
                          '– начинаться с __заглавной буквы__,\n'
                          '– содержать только __кирилицу__,\n'
                          '– иметь максимальную длину __75 символов__\.',
                     parse_mode='MarkdownV2')
        return None

    try:
        user = user_service.get_new_user(command_string=message.text)
        answer_text = 'Пользователь успешно создан.'
    except exceptions.AlreadyExist:
        answer_text = 'Пользователь с заданным сочетанием имени и фамилии уже существует!'

    bot.send_message(chat_id=message.chat.id, text=answer_text)


@bot.message_handler(commands=['delete_user'])
@admin_required
def delete_user(message: types.Message):
    """Удаляет пользователя по ID"""

    # ID пользователя может быть только числом.
    # Пример: /delete_user 12
    if not re.fullmatch(r'^/delete_user [0-9]+$', message.text):
        bot.reply_to(message, '*Неверная команда\!*\n`\/delete\_user \{user\_id\}`\n'
                              'ID пользователя можно узнать с помощью команды \/users\_list',
                     parse_mode='MarkdownV2')
        return None

    try:
        user_info = user_service.delete_user(command_string=message.text)
        answer_text = f'Удален пользователь:\n' \
                      f'{user_info.last_name} {user_info.first_name}'
    except exceptions.NotExist:
        answer_text = 'Пользователь с заданным ID не существует!'
    except exceptions.BadNumberOfArgs:
        answer_text = 'Неверное количество аргументов команды!'
    except exceptions.BadArgsTypes:
        answer_text = 'ID пользователя должно быть числом!'

    bot.send_message(chat_id=message.chat.id, text=answer_text)


@bot.message_handler(regexp=r"^/setup_user_model$")
@admin_required
def setup_user_model(message: types.Message):
    bot.send_message(chat_id=message.chat.id,
                     text='Функционал недоступен!')
