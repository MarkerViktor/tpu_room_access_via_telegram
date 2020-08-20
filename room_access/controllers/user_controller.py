from telebot import types

from room_access.app import bot
from room_access.services import user_service
from room_access.utils import admin_required


@bot.message_handler(commands=['users_list'])
@admin_required
def users_list(message: types.Message):
    """
    Выполняется при получении команды /users_list .
    Отвечает сообщением со списком всех пользователей и их ID
    """
    users = user_service.get_all_users_short_info()

    answer_string = f"*В системе зарегистрировано пользователей — {len(users)}:*\n" \
                    "`\{user\_id\} : \{last\_name\} \{first\_name\}`\n"

    for user in users:
        answer_string += f'{user.id} : {user.last_name} {user.first_name}\n'

    bot.send_message(chat_id=message.chat.id, text=answer_string, parse_mode='MarkdownV2')
