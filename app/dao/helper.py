"""Модуль, описывающий декоратор для повторного подключения к БД"""


from functools import wraps
import asyncio
from sqlalchemy.exc import SQLAlchemyError


MAX_RETRIES = 5
RETRY_DELAY = 2


def retry_db_connect(function):
    """Функция, реализующая декоратор для повторных подключений к БД"""
    @wraps(function)
    async def wrapper(*args, **kwargs):
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                return await function(*args, **kwargs)
            except SQLAlchemyError as e:
                print(f"Попытка {attempt} из {MAX_RETRIES}")
                if attempt == MAX_RETRIES:
                    raise
                await asyncio.sleep(RETRY_DELAY)
    return wrapper