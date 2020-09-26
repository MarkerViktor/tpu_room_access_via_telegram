import logging
from typing import Tuple, List

import requests


def prepare_command_args(message_text: str) -> tuple:
    """Принимает строку, содержащую текст сообщения c командой,
    возвращает кортеж со всеми аргументами, разделенными пробелами"""
    words: List[str] = message_text.split(' ')
    words.pop(0)

    args = []
    for word in words:
        try:
            args.append(int(word))
        except ValueError:
            args.append(word)
    return tuple(args)


# Не закончено
def logger(func):
    """Декоратор. Ловит все исключения, логирует их и опять выбрасывает исключение."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
