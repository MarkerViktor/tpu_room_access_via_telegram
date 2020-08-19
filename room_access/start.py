from aiogram import executor

from room_access.app import dp


if __name__ == '__main__':
    executor.start_polling(dp)
