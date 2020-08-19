import logging

from aiogram import Bot, Dispatcher
from pony.orm import Database

from room_access import config


# Настройка логирования
logging.basicConfig(
    filename=config.LOG_PATH,
    level=logging.DEBUG,
)

# Инициализация сущностей бота и диспетчера
bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher(bot)

# Импорт обработчиков команд
from room_access.controllers import UserController


# Инициализация БД
db = Database()
db.bind(provider='sqlite', filename=config.DB_PATH)

# Импорт сущностей
from room_access import entities


db.generate_mapping()



