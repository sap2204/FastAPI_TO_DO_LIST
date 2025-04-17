"""Модуль, реализующий декоратор для логирования функций"""

from functools import wraps

from loguru import logger


def log_function(func):
    """Функция, реализующая декоратор для логирования"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Вызов {func.__qualname__} с args={args}, kwargs={kwargs}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"{func.__qualname__} успешно выполнена")
            return result
        except Exception as e:
            logger.error(f"Ошибка в {func.__qualname__}: {e}")
            raise

    return wrapper
