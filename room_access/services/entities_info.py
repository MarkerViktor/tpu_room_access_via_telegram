from typing import NamedTuple


class UserInfo(NamedTuple):
    """Краткая информация о пользователе"""
    id: int
    first_name: str
    last_name: str


class AdminInfo(NamedTuple):
    """Краткая информация о администраторе"""
    id: int
    telegram_username: str


class RoomInfo(NamedTuple):
    """Краткая информация о помещении"""
    id: int
    location: str

