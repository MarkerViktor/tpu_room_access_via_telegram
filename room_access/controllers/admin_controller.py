import re

from telebot import types

from room_access.app import bot
from room_access.services import admin_sevice, exceptions
from room_access.controllers.utils import admin_required


@bot.message_handler(commands=['admins_list'])
def admins_list(message: types.Message):
    admins = admin_sevice.admins_list()

    answer_text = f"Всего администраторов — {len(admins)}\n" \
                  "`\{admin\_id\} : @username\n`"

    for admin in admins:
        answer_text += f'{admin.id} : @{admin.telegram_username}\n'

    bot.send_message(chat_id=message.chat.id, text=answer_text, parse_mode='MarkdownV2')


@bot.message_handler(commands=['new_admin'])
@admin_required
def new_admin(message: types.Message):
    """Добавляет нового администратора"""

    # Ник администратора должен начинаться с символа "@",
    # содержать только цифры и латинские буквы, иметь длину > 5 символов
    # Пример команды: /new_admin @MarkerViktor
    if not re.fullmatch(r'^/new_admin @[A-Za-z0-9]{5,32}$', message.text):
        bot.reply_to(message,
                     text='*Неверная команда\!*\n`\/new\_admin \@\{telegram\_username\}`\n'
                          'Ник должен\n'
                          '– начинаться с символа __\@__,\n'
                          '– содержать только __латиницу__, __цифры__ и __нижние подчеркивания,__\n'
                          '– иметь длину __от 5 до 32 символов__\.',
                     parse_mode='MarkdownV2')
        return None

    try:
        admin_sevice.new_admin(command_string=message.text)
        answer_text = 'Администратор успешно добавлен.'
    except exceptions.AlreadyExist:
        answer_text = 'Администратор с указанным ником уже существует!'
    except exceptions.BadNumberOfArgs:
        answer_text = 'Неверное количество аргументов команды!'
    except exceptions.BadArgs:
        answer_text = 'Неверный формат аргументов команды!'

    bot.send_message(chat_id=message.chat.id, text=answer_text)


@bot.message_handler(commands=['delete_admin'])
@admin_required
def delete_admin(message: types.Message):
    """Удаляет администратора"""

    # ID администратора может быть только числом.
    # Пример: /delete_admin 12
    if not re.fullmatch(r'^/delete_admin [0-9]+$', message.text):
        bot.reply_to(message, '*Неверная команда\!*\n`\/delete\_admin \{admin\_id\}`\n'
                              'ID администратора можно узнать с помощью команды \/admins\_list',
                     parse_mode='MarkdownV2')
        return None

    try:
        admin_sevice.delete_admin(command_string=message.text)
        answer_text = ''
    except exceptions.NotExist:
        pass

    bot.send_message(chat_id=message.chat.id, text=answer_text)

