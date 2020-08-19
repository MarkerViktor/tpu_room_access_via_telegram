import logging

from aiogram import Bot, Dispatcher
from pony.orm import Database

from room_access import config
from room_access import entities


# Настройка логирования
logging.basicConfig(
    filename=config.LOG_PATH,
    level=logging.DEBUG,
)

# Инициализация сущностей бота и диспетчера
bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher(bot)

# Импорт обработчиков команд
from room_access.controllers import user_controller


# Инициализация БД
entities.db.bind(provider='sqlite', filename=config.DB_PATH)
entities.db.generate_mapping()



