from datetime import datetime

from pony.orm import *


db = Database()

sql_debug(True)

class User(db.Entity):
    """Пользователь системы контроля доступа"""
    id = PrimaryKey(int, auto=True)
    first_name = Required(str, 75)  # Имя пользователя
    last_name = Optional(str, 75)  # Фамилия пользователя
    visits = Set('Visit')  # Посещения пользователя
    allowed_rooms = Set('Room')  # Помещения, в которые разрешен доступ пользователю


class Room(db.Entity):
    """Помещение, в котором контролируется доступ"""
    location = PrimaryKey(str)  # Местоположение помещения
    visits = Set('Visit')  # Посещения помещения
    allowed_users = Set(User)  # Пользователи, которым разрешен доступ к помещению
    admins = Set('Admin')  # Администраторы, имеющие право управлять доступом в данном помещении


class Visit(db.Entity):
    """Посещение пользователем помещения в конкретное время"""
    id = PrimaryKey(int, auto=True)
    datetime = Required(datetime)  # Время посещения
    visited_room = Required(Room)  # Помещение, которое посетили
    visitor = Required(User)  # Посетитель


class Admin(db.Entity):
    """Администратор помещений"""
    telegram_username = PrimaryKey(str)  # имя пользователя администратора в телеграм
    managed_rooms = Set(Room)  # Помещения, доступом в которые имеет право управлять данный администратор



