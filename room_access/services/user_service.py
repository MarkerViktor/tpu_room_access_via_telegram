from collections import namedtuple
from asyncio import get_event_loop

from pony.orm import select, db_session
from pony.orm.core import QueryResult

from room_access.entities import User

UserShortInfo = namedtuple('UserShortInfo', ('id', 'first_name', 'last_name'))

@db_session
def get_all_users_short_info():
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


