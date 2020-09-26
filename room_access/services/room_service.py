from collections import namedtuple
from typing import Tuple, NamedTuple

from pony import orm

from room_access.entities import Room, Admin
from room_access.services import exceptions
from room_access.services.entities_info import RoomInfo, AdminInfo, UserInfo


@orm.db_session
def get_all_rooms() -> Tuple[RoomInfo, ...]:
    """Получить кортеж с информацией о всех помещениях"""
    rooms = orm.select(room for room in Room)[:]
    return tuple(RoomInfo(room.id, room.location) for room in rooms)


@orm.db_session
def check_room_admin(room_id: int, telegram_username: str) -> bool:
    """Проверяет, входит ли указанный админимтратор в список администраторов указанной камнаты"""
    return Admin.get(telegram_username=telegram_username) in Room.get(id=room_id).admins


@orm.db_session
def get_room_admins(room_id: int) -> Tuple[AdminInfo, ...]:
    """Получить кортеж с информацией о всех администраторах помещения"""
    try:
        room: Room = Room[room_id]
    except orm.ObjectNotFound as e:
        raise exceptions.NotExist(e)
    return tuple(AdminInfo(admin.id, admin.telegram_username) for admin in room.admins)


@orm.db_session
def add_admin_to_room(room_id: int, admin_id: int) -> None:
    """Добавляет администратора указанному помещению"""
    try:
        admin: Admin = Admin[admin_id]
        room: Room = Room[room_id]
    except orm.ObjectNotFound as e:
        raise exceptions.NotExist(e)

    if admin in room.admins:
        raise exceptions.AlreadyExist("The admin has already in admins of the room")

    room.admins.add(admin)


@orm.db_session
def delete_admin_from_room(room_id: int, admin_id: int) -> None:
    """Удаляет администратора из указанного помещения"""
    try:
        admin: Admin = Admin[admin_id]
        room: Room = Room[room_id]
    except orm.ObjectNotFound as e:
        raise exceptions.NotExist(e)

    if admin not in room.admins:
        raise exceptions.BaseServiceException("The admin is not in admins of the room")

    room.admins.remove(admin)

@orm.db_session
def get_allowed_users(room_id) -> Tuple[UserInfo, ...]:
    """Получение кортежа с краткой информацией о пользователях, имеющих доступ в аудиторию"""
    try:
        room: Room = Room[room_id]
    except orm.ObjectNotFound as e:
        raise exceptions.NotExist(e)

    allowed_users = room.allowed_users
    return tuple(UserInfo(user.id, user.first_name, user.last_name) for user in allowed_users)