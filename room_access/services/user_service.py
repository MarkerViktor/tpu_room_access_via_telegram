from collections import namedtuple
from typing import Tuple

from pony.orm import select, db_session, ObjectNotFound

from room_access.utils import prepare_command_args
from room_access import exceptions

from room_access.repositories import user_repository


UserShortInfo = namedtuple(typename='UserShortInfo',
                           field_names=('id', 'first_name', 'last_name'))

def new_user(command_string: str) -> None:
    """Создание нового пользователя"""
    args: tuple = prepare_command_args(command_string)  # (last_name, first_name)

    try:
        last_name, first_name = args
    except ValueError:
        raise exceptions.BadNumberOfArgs()

    try:
        user_repository.create_user_entity(first_name, last_name)
    except TypeError:
        raise exceptions.BadArgType()


def delete_user(command_string: str) -> UserShortInfo:
    """Удаление пользователя и получение информации о нем"""
    args: tuple = prepare_command_args(command_string)  # (user_id)
    try:
        user_id = args[0]
    except IndexError:
        raise exceptions.BadNumberOfArgs()

    try:
        user = user_repository.get_user_by_id(user_id)
    except ObjectNotFound:
        raise exceptions.NotExist()
    user_info = UserShortInfo(None, user.first_name, user.last_name)

    user_repository.delete_user_by_id(user_id)
    return user_info


def users_list() -> Tuple[UserShortInfo]:
    """
    Получение информации обо всех пользователях
    в виде namedtuple с атрибутами id, first_name, last_name
    """
    users = user_repository.get_all_users()
    return tuple(map(lambda user: UserShortInfo(last_name=user.last_name,
                                                first_name=user.first_name,
                                                id=user.id), users))


if __name__ == '__main__':
    from room_access.entities import db

    db.bind(provider='sqlite', filename='C:/Users/markerviktor/Desktop/tpu_room_access_via_telegram/db.sqlite')
    db.generate_mapping()
