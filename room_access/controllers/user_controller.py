from telebot import types

from room_access.app import bot
from room_access.services import user_service
from room_access import exceptions
from room_access.controllers.utils import admin_required


@bot.message_handler(commands=['users_list'])
@admin_required
def users_list(message: types.Message):
    """
    Выполняется при получении команды /users_list .
    Отвечает сообщением со списком всех пользователей и их ID
    """
    users: tuple = user_service.users_list()

    answer_string = f"*Всего пользователей — {len(users)}:*\n" \
                    "`\{user\_id\} : \{last\_name\} \{first\_name\}`\n"

    for user in users:
        answer_string += f'{user.id} : {user.last_name} {user.first_name}\n'

    bot.send_message(chat_id=message.chat.id, text=answer_string, parse_mode='MarkdownV2')


@bot.message_handler(commands=['new_user'])
@admin_required
def new_user(message: types.Message):
    """Создает нового пользователя"""
    try:
        user_service.new_user(command_string=message.text)
        answer_text = 'Пользователь успешно создан.'
    except exceptions.AlreadyExist:
        answer_text = 'Пользователь с заданным сочетанием имени и фамилии уже существует!'
    except exceptions.BadArgType:
        answer_text = 'Фамилия или имя не могут состоять только из цифр!'
    except exceptions.BadNumberOfArgs:
        answer_text = 'Неверное количество аргументов команды!'

    bot.send_message(chat_id=message.chat.id, text=answer_text)


@bot.message_handler(commands=['delete_user'])
@admin_required
def delete_user(message: types.Message):
    """Удаляет пользователя по ID"""
    try:
        user_info = user_service.delete_user(command_string=message.text)
        answer_text = f'Удален пользователь:\n' \
                      f'{user_info.last_name} {user_info.first_name}'
    except exceptions.NotExist:
        answer_text = 'Пользователь с заданным ID не существует!'
    except exceptions.BadNumberOfArgs:
        answer_text = 'Неверное количество аргументов команды!'
    except exceptions.BadArgType:
        answer_text = 'ID пользователя должно быть числом!'

    bot.send_message(chat_id=message.chat.id, text=answer_text)


@bot.message_handler(commands=['setup_user_model'])
@admin_required
def setup_user_model(message:types.Message):
    bot.send_message(chat_id=message.chat.id,
                     text='Функционал недоступен!')
