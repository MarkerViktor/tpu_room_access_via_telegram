from collections import namedtuple
from typing import Tuple

from pony.orm import select, db_session

from room_access.entities import User
from room_access.utils import prepare_command_args


class UserAlreadyExist(Exception):
    """Попытка создать пользователя, который уже существует"""
    pass

class BadUserCreatingParams(Exception):
    """Проблема с параметрами запроса создания пользователя"""
    pass

class BadUserCreatingParamsTypes(BadUserCreatingParams):
    """Проблема с типом параметров запроса создания пользователя"""
    pass


@db_session
def create_user_entity(first_name: str, last_name: str) -> User:
    """Добавляет в БД нового пользователя"""
    old_user = User.get(first_name=first_name, last_name=last_name)
    if old_user is None:
        return User(first_name=first_name, last_name=last_name)
    else:
        raise UserAlreadyExist(f'User with such combination of first and last names'
                               f' ({last_name} {first_name}) is already exist!')

def new_user(command_string: str) -> None:
    """Создание нового пользователя"""
    args: tuple = prepare_command_args(command_string)

    try:
        create_user_entity(first_name=args[1], last_name=args[0])
    except TypeError:
        raise BadUserCreatingParamsTypes
    except IndexError:
        raise BadUserCreatingParams


def delete_user(command_string: str):
    args: tuple = prepare_command_args(command_string)


UserShortInfo = namedtuple(typename='UserShortInfo',
                           field_names=('id', 'first_name', 'last_name'))

@db_session
def users_list() -> Tuple[UserShortInfo]:
    """
    Получение информации обо всех пользователях
    в виде namedtuple с атрибутами id, first_name, last_name
    """
    users = select((user.id, user.first_name, user.last_name) for user in User)[:]
    return tuple(map(lambda user: UserShortInfo(*user), users))


if __name__ == '__main__':
    from room_access.entities import db

    db.bind(provider='sqlite', filename='C:/Users/markerviktor/Desktop/tpu_room_access_via_telegram/db.sqlite')
    db.generate_mapping()
