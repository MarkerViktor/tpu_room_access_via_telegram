import re
from typing import Tuple

from telebot import types

from room_access.app import bot
from room_access.services import room_service
from room_access.services import exceptions
from room_access.controllers.utils import admin_required
from room_access.services.entities_info import UserInfo


@bot.message_handler(commands=['rooms_list'])  # /rooms_list
def rooms_list(message: types.Message):
    """Отвечает сообщением со списком всех помещений и их ID"""
    rooms: Tuple[room_service.RoomInfo] = room_service.get_all_rooms()

    answer_string = f"*Всего помещений — {len(rooms)}:*\n" \
                    "`\{room\_id\} : \{room_location\}`\n"

    for room in rooms:
        answer_string += f'{room.id} : {room.location}\n'

    bot.send_message(chat_id=message.chat.id, text=answer_string, parse_mode='MarkdownV2')


@bot.message_handler(commands=['room_admins_list'])  # /room_admins_list {room_id}
def room_admins_list(message: types.Message):
    """Получить список администраторов помещения"""

    command_match = re.fullmatch(r"^(?P<command>/room_admins_list)\s(?P<room_id>\d+)$", message.text)
    if not command_match:
        bot.reply_to(message,
                     text='*Неверная команда\!*\n`\/room\_admins\_list \{room\_id\}`\n'
                          'ID помещения можно узнать с помощью команды \/rooms\_list\.',
                     parse_mode='MarkdownV2')
        return

    room_id = int(command_match['room_id'])

    try:
        room_admins = room_service.get_room_admins(room_id)
        answer_text = f"Администраторов помещения — {len(room_admins)}\n" \
                      "`\{admin\_id\} : @username\n`"
        for admin in room_admins:
            answer_text += f'{admin.id} : @{admin.telegram_username}\n'
    except exceptions.NotExist:
        answer_text = "Помещение с указанным ID не существует\."
    bot.send_message(chat_id=message.chat.id, text=answer_text, parse_mode='MarkdownV2')


@bot.message_handler(commands=['add_room_admin'])  # /add_room_admin {room_id} {admin_id}
@admin_required
def add_room_admin(message: types.Message):
    """Дает указанному администратору право управлением доступом в помещение"""

    # Регулярное выражение, соответствующее команде "/add_room_admin {room_id} {admin_id}",
    # разделенное на именнованные группы command, room_id, admin_id
    command_match = re.fullmatch(r"^(?P<command>/add_room_admin)\s(?P<room_id>\d+)\s(?P<admin_id>\d+)$", message.text)
    if not command_match:
        bot.reply_to(message,
                     text='*Неверная команда\!*\n`\/add\_room\_admin \{room\_id\} \{admin\_id\}`\n'
                          'ID помещения можно узнать с помощью команды \/rooms\_list ,\n'
                          'ID администратора можно узнать с помощью команды \/admins\_list \.',
                     parse_mode='MarkdownV2')
        return

    room_id, admin_id = int(command_match['room_id']), int(command_match['admin_id'])

    # Проверка на то, что запрос от администратора указанного помещения
    if not room_service.check_room_admin(room_id, message.from_user.username):
        bot.send_message(chat_id=message.chat.id,
                         text='Вы не входите в список администраторов указанного помещения\n'
                              'Чтобы добавить администратора, нужно входить в список администраторов помешения')
        return

    try:
        room_service.add_admin_to_room(room_id, admin_id)
        answer_string = "Администратор успешно добавлен\."
    except exceptions.NotExist:
        answer_string = "Для помещения или администратора указан неверный ID\."
    except exceptions.AlreadyExist:
        answer_string = "Указанный администратор уже входит в список администраторов указанного помещения\."

    bot.send_message(chat_id=message.chat.id, text=answer_string, parse_mode='MarkdownV2')


@bot.message_handler(commands=['delete_room_admin'])  # /delete_room_admin {room_id} {admin_id}
@admin_required
def delete_room_admin(message: types.Message):
    """Удаляет указанного администратора из списка администраторов указанного помещения"""

    # Регулярное выражение, соответствующее команде "/delete_room_admin {room_id} {admin_id}",
    # разделенное на именнованные группы command, room_id, admin_id
    command_match = re.fullmatch(r"^(?P<command>/delete_room_admin)\s(?P<room_id>\d)\s(?P<admin_id>\d)", message.text)
    if not command_match:
        bot.reply_to(message,
                     text='*Неверная команда\!*\n`\/delete\_room\_admin \{room\_id\} \{admin\_id\}`\n'
                          'ID помещения можно узнать с помощью команды \/rooms\_list ,\n'
                          'ID администратора можно узнать с помощью команды \/admins\_list \.',
                     parse_mode='MarkdownV2')
        return

    room_id, admin_id = int(command_match['room_id']), int(command_match['admin_id'])

    # Проверка на то, что запрос от администратора указанного помещения
    if not room_service.check_room_admin(room_id, message.from_user.username):
        bot.send_message(chat_id=message.chat.id,
                         text='Вы не входите в список администраторов указанного помещения.\n'
                              'Чтобы удалить администратора, нужно входить в список администраторов помешения')
        return

    try:
        room_service.delete_admin_from_room(room_id, admin_id)
        answer_string = "Администратор удален\."
    except exceptions.NotExist:
        answer_string = "Для помещения или администратора указан неверный ID\."

    bot.send_message(chat_id=message.chat.id, text=answer_string, parse_mode='MarkdownV2')


@bot.message_handler(commands=['allowed_users_list'])  # /allowed_users_list {room_id}
@admin_required
def allowed_users_list(message: types.Message):
    """Получить список пользователей, которым разрешен доступ в указанное помещение"""

    # Регулярное выражение, соответствующее команде "/allowed_users_list {room_id}",
    # разделенное на именнованные группы command, room_id
    command_match = re.fullmatch(r"^(?P<command>/allowed_users_list)\s(?P<room_id>\d)$", message.text)
    if not command_match:
        bot.reply_to(message,
                     text='*Неверная команда\!*\n`\/allowed\_users\_list \{room\_id\}`\n'
                          'ID помещения можно узнать с помощью команды \/rooms\_list\.',
                     parse_mode='MarkdownV2')
        return

    room_id = int(command_match['room_id'])

    try:
        allowed_users: Tuple[UserInfo, ...] = room_service.get_allowed_users(room_id)

        answer_string = f"*Разрешенных пользователей — {len(allowed_users)}:*\n" \
                        r"`\{user\_id\} : \{last\_name\} \{first\_name\}`\n"
        for user in allowed_users:
            answer_string += f'{user.id} : {user.last_name} {user.first_name}\n'

    except exceptions.NotExist:
        answer_string = r"Помещение с указанным ID не существует\."

    bot.send_message(chat_id=message.chat.id, text=answer_string, parse_mode='MarkdownV2')