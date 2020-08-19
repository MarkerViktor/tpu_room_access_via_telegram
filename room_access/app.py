import logging

from aiogram import Bot, Dispatcher, executor

from room_access import config
from room_access.entities import connect_db


# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация сущностей бота и диспетчера
bot = Bot(token=config.TG_TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    connect_db()

