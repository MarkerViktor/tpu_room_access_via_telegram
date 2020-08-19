from aiogram import types

from room_access.app import dp

@dp.message_handler(commands=['users_list'])
async def get_users_list(message: types.Message):
    pass
