"""Модуль, описывающий работу  хеширования паролей и аутентификации"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Функция для хеширования пароля"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Функция проверки пароля"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Функция формирования JWT-токена"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    """Функция, возвращающая пользователя при удачной аутентификации"""
    user = await UsersDAO.find_one_or_none(email=email)
    if user and verify_password(password, user.password):
        return user
