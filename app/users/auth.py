"""Модуль, описывающий работу  хеширования паролей и аутентификации"""

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt
from loguru import logger
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_password_complexity(password: str) -> str:
    """Функция, реализующая проверку сложности пароля"""
    logger.info(f"Проверка пароля {password} на сложность")
    if len(password) < 5 or not all(
        char.isalnum() and char.isascii() for char in password
    ):
        logger.error(f"Проверка пароля {password} на сложность не прошла")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пароль должен быть минимум 5 символов (цифры, латинские буквы)"
        )
    logger.info(f"Проверка пароля {password} на сложность прошла")
    return password


def get_password_hash(password: str) -> str:
    """Функция для хеширования пароля"""
    check_password_complexity(password)
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Функция проверки пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt(data: dict, **kwargs) -> str:
    """Функция формирования jwt токена"""
    logger.info(f"Формирование jwt с данными {data}")
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(**kwargs)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    logger.info(f"jwt c {data} сформирован")
    return encoded_jwt


def create_access_token(data: dict) -> str:
    """Функция формирования access JWT-токена"""
    return create_jwt(data, minutes=30)


def create_refresh_token(data: dict) -> str:
    """Функция формирования refresh JWT-токена"""
    return create_jwt(data, days=30)


async def authenticate_user(email: EmailStr, password: str):
    """Функция, возвращающая пользователя при удачной аутентификации"""
    logger.info(f"Поиск пользователя по emal {email}")
    user = await UsersDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.password):
        logger.info(f"Пользователь с {email} найден")
        return user
