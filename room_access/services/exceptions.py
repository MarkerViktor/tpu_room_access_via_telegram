from room_access.base_exception import BaseProjectException

class BaseServiceException(BaseProjectException):
    """Базовое исключение"""
    pass


#  Параметры команд

class BadArgs(BaseException):
    """Проблема с параметрами команды"""

class BadNumberOfArgs(BadArgs):
    """Неверное количество аргументов"""
    pass

class BadArgsTypes(BadArgs):
    """Неверный тип аргумента"""
    pass


#  Сущности
class AlreadyExist(BaseServiceException):
    """Сущность уже существует (дублирует существующую)"""
    pass

class NotExist(BaseServiceException):
    """Запрашиваемая сущность не существует"""
    pass
