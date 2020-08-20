from asyncio import get_event_loop

from pony.orm import db_session, select, exists
from telebot.types import Message

from room_access.entities import Admin

@db_session
def check_admin_username_exist(username: str) -> bool:
    """Проверяет, существует ли администратор с указанным именем пользователя"""
    return Admin.get(telegram_username=username) is not None


if __name__ == '__main__':
    from room_access.entities import db

    db.bind(provider='sqlite', filename='C:/Users/markerviktor/Desktop/tpu_room_access_via_telegram/db.sqlite')
    db.generate_mapping()

    print(check_admin_username_exist('MarkerViktor'))
