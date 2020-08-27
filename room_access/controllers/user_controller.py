from telebot import types

from room_access.app import bot
from room_access.services import user_service
from room_access.utils import admin_required, prepare_command_args


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
    except user_service.UserAlreadyExist:
        answer_text = 'Пользователь с заданным очетанием имени и фамилии уже существует!'
    except user_service.BadUserCreatingParamsTypes:
        answer_text = 'Фамилия или имя не могут состоять только из цифр!'
    except user_service.BadUserCreatingParams:
        answer_text = 'Неверный формат параметров команды создания пользователя!'

    bot.send_message(chat_id=message.chat.id, text=answer_text)


@bot.message_handler(commands=['delete_user'])
@admin_required
def delete_user(message: types.Message):
    """Удаляет пользователя по ID"""
    pass
