from typing import Tuple

from pony.orm import select, db_session, ObjectNotFound

from room_access.entities import Admin
from room_access.repositories import exceptions


@db_session
def create_admin_entity(telegram_username: str) -> Admin:
    """
    Создание сущности администратора, сохранение ее в БД и
    возвращение объекта администратора
    """
    try:
        return Admin(telegram_username=telegram_username)
    except TypeError as e:
        raise exceptions.BadValuesTypes(e)

@db_session
def get_all_admins() -> Tuple[Admin]:
    """
    Запрос из БД всех записей из таблицы Admins
    """
    return tuple(select(admin for admin in Admin)[:])

@db_session
def get_admin_by_id(admin_id: int) -> Admin:
    """
    Получить сущность администратора по id
    """
    try:
        return Admin[admin_id]
    except ObjectNotFound as e:
        raise exceptions.EntityNotFound(e)

@db_session
def admin_exist_by_username(telegram_username: str) -> bool:
    """
    Проверка существования администратора с указанным именем пользователя
    """
    return Admin.get(telegram_username=telegram_username) is not None

@db_session
def delete_admin_by_id(admin_id: int) -> None:
    """
    Удаляет сущность пользователя из БД
    """
    get_admin_by_id(admin_id).delete()
