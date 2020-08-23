from pony.orm import db_session, select, exists

from room_access.entities import Admin


@db_session
def get_admin_by_id(admin_id: int) -> Admin:
    """Возваращет сущность администратора по его ID"""
    return Admin.get(id=admin_id)

@db_session
def get_admin_by_username(username: str) -> Admin:
    """Возвращает сущность администратора по имени пользователя в телеграм"""
    return Admin.get(telegram_username=username)

@db_session
def check_admin_exist_by_username(username: str) -> bool:
    """Проверяет, существует ли администратор с указанным именем пользователя"""
    return get_admin_by_username(username) is not None


if __name__ == '__main__':
    from room_access.entities import db

    db.bind(provider='sqlite',
            filename='C:/Users/markerviktor/Desktop/tpu_room_access_via_telegram/db.sqlite')
    db.generate_mapping()
