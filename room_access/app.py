import logging
from concurrent.futures import ThreadPoolExecutor

from telebot import TeleBot

from room_access import config
from room_access import entities


# Настройка логирования
logging.basicConfig(
    #filename=config.LOG_PATH,
    level=logging.DEBUG,
)


# Инициализация сущностей бота
bot = TeleBot(
    token=config.TG_TOKEN,
    threaded=True,
    num_threads=2
)

# Импорт обработчиков команд
from room_access.controllers import user_controller
from room_access.controllers import help_controller


# Инициализация БД
entities.db.bind(provider='sqlite', filename=config.DB_PATH)
entities.db.generate_mapping()



