

class BaseServiceException(Exception):
    """Базовое исключение"""
    pass


#  Параметры команд
class BadNumberOfArgs(BaseServiceException):
    """Неверное количество аргументов"""
    pass

class BadArgType(BaseServiceException):
    """Неверный тип аргумента"""
    pass


#  Сущности
class AlreadyExist(BaseServiceException):
    """Сущность уже существует (дублирует существующую)"""
    pass

class NotExist(BaseServiceException):
    """Запрашиваемая сущность не существует"""
    pass
