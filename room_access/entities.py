from datetime import datetime
from pony.orm import *

from room_access.config import DB_LOCATION

db = Database()

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    first_name = Required(str, 75)  # Имя
    last_name = Optional(str, 75)  # Фамилия
    visits = Set('Visit')
    allowed_rooms = Set('Room')
    groups = Set('Group')

class Admin(User):
    telegram_id = Required(str)
    managed_rooms = Set('Room')

class Student(User):
    study_group = Required('StudyGroup')

class Group(db.Entity):
    name = PrimaryKey(str)
    users = Set('User')
    allowed_rooms = Set('Room')

class StudyGroup(Group):
    students = Set('Student')
    institute = Optional(str)
    department = Optional(str)
    course_number = Optional(str)

class Room(db.Entity):
    location = PrimaryKey(str)
    visits = Set('Visit')
    allowed_users = Set('User')
    allowed_user_groups = Set('Group')
    admins = Set('Admin')

class Visit(db.Entity):
    id = PrimaryKey(int, auto=True)
    datetime = Required(datetime)
    visited_room = Required('Room')
    visitor = Required('User')

def connect_db():
    db.bind(provider='sqlite', filename=DB_LOCATION)
    db.generate_mapping()
    return db
