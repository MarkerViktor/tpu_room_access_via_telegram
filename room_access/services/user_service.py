from collections import namedtuple
from typing import Tuple

from room_access.services.entities_info import UserInfo
from room_access.utils import prepare_command_args
from room_access.services import exceptions as service_exceptions
from room_access.repositories import user_repository
from room_access.repositories import exceptions as repo_exceptions


def get_new_user(command_string: str) -> None:
    """Создание нового пользователя"""
    args: tuple = prepare_command_args(command_string)  # (last_name, first_name)
    try:
        last_name, first_name = args
    except ValueError:
        raise service_exceptions.BadNumberOfArgs()

    try:
        if user_repository.user_exist_by_first_and_last_name(first_name, last_name):
            raise service_exceptions.AlreadyExist()
        user_repository.create_user_entity(first_name, last_name)
    except repo_exceptions.BadValuesTypes:
        raise service_exceptions.BadArgsTypes()


def delete_user(command_string: str) -> UserInfo:
    """Удаление пользователя и получение информации о нем"""
    args: tuple = prepare_command_args(command_string)  # (user_id)
    try:
        user_id: int = args[0]
    except IndexError:
        raise service_exceptions.BadNumberOfArgs()

    try:
        user = user_repository.get_user_by_id(user_id)
    except repo_exceptions.EntityNotFound:
        raise service_exceptions.NotExist()
    user_info = UserInfo(None, user.first_name, user.last_name)

    user_repository.delete_user_by_id(user_id)
    return user_info


def get_all_users() -> Tuple[UserInfo]:
    """
    Получение информации обо всех пользователях
    в виде namedtuple с атрибутами id, first_name, last_name
    """
    users = user_repository.get_all_users()
    return tuple(map(lambda user: UserInfo(last_name=user.last_name,
                                           first_name=user.first_name,
                                           id=user.id), users))


if __name__ == '__main__':
    from room_access.entities import db

    db.bind(provider='sqlite', filename='C:/Users/markerviktor/Desktop/tpu_room_access_via_telegram/db.sqlite')
    db.generate_mapping()
