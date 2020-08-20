from telebot.types import Message

from room_access.app import bot
from room_access.services.admin_sevice import check_admin_username_exist


def admin_required(controller):
    """Декоратор. Проверка на то, что сообщение от администратора"""
    def wrapper(message: Message):
        if check_admin_username_exist(message.from_user.username):
            return controller(message)
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='❌ Вы не являетесь администратором, доступ запрещен!'
            )
    return wrapper
