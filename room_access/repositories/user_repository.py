from typing import Tuple, Optional

from pony.orm import select, db_session, ObjectNotFound

from room_access.entities import User


@db_session
def create_user_entity(first_name: str, last_name: str) -> User:
    """Создание сущности пользователя, сохранение ее в БД и
    возвращение объекта пользователя"""
    return User(first_name=first_name, last_name=last_name)

@db_session
def get_all_users() -> Tuple[User]:
    """Запрос из БД всех записей из таблицы Users"""
    return tuple(select(user for user in User)[:])

@db_session
def get_user_by_id(user_id: int) -> User:
    """Получить сущность пользователя по id"""
    return User[user_id]

@db_session
def user_exist_by_first_and_last_name(first_name: str, last_name: str) -> bool:
    """Существует ли пользователь с указанными именем и фамилией"""
    return User.get(first_name=first_name, last_name=last_name) is not None

@db_session
def delete_user_by_id(user_id: int) -> None:
    """Удаляет сущность пользователя из БД"""
    User[user_id].delete()