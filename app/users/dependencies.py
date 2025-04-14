"""Модуль, описывающий получение токена из запроса и излечение пользователя из токена"""

from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
    """Функция, возвращающа токен из запроса"""
    token = request.cookies.get("todolist_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутствует JWT-токен"
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Функция, возвращающая пользователя из токена"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена"
        )
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Время токена истекло"
        )
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден пользователь"
        )
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден пользователь"
        )

    return user
