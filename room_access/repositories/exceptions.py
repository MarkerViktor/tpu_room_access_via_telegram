""" Исключения модулей работы с БД """

from room_access.base_exception import BaseProjectException


class BaseRepositoryException(BaseProjectException):
    """
    Базовое исключение модуля работы с БД
    """
    pass

class EntityNotFound(BaseRepositoryException):
    """
    Заказанная сущность не существует
    """
    pass

class BadValuesTypes(BaseRepositoryException):
    """
    Неверные типы для указанных колонок
    """
    pass
