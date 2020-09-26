from typing import Tuple

from pony import orm

from room_access.services import exceptions as service_exceptions
from room_access.services.entities_info import AdminInfo
from room_access.utils import prepare_command_args
from room_access.repositories import admin_repository


def admins_list() -> Tuple[AdminInfo]:
    """
    Получение информации обо всех администраторах
    в виде namedtuple с атрибутами id, telegram_username
    """
    admins = admin_repository.get_all_admins()
    return tuple(map(lambda admin: AdminInfo(id=admin.id, telegram_username=admin.telegram_username), admins))


def new_admin(command_string: str):
    """Создание нового администратора"""
    args = prepare_command_args(command_string)  # (username)
    try:
        username: str = args[0]
    except IndexError:
        raise service_exceptions.BadNumberOfArgs()

    # проверка на символ "@" в начале имени пользователя
    if username.startswith('@'):
        username = username[1:]
    else:
        raise service_exceptions.BadArgs()

    if admin_repository.admin_exist_by_username(username):
        raise service_exceptions.AlreadyExist()

    admin_repository.create_admin_entity(username)


def delete_admin(command_string: str) -> AdminInfo:
    """Удаление администратора и возвращение информации о нем"""
    args = prepare_command_args(command_string)  # (admin_id)
    try:
        admin_id = args[0]
    except IndexError:
        raise service_exceptions.BadNumberOfArgs


if __name__ == '__main__':
    from room_access.entities import db, Admin, Room

    db.bind(provider='sqlite',
            filename='C:/Users/markerviktor/Desktop/tpu_room_access_via_telegram/db.sqlite')
    db.generate_mapping()
