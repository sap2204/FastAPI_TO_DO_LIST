"""Модуль, описывающий получение токена из запроса и излечение пользователя из токена"""

from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request, Response, status
from jose import JWTError, jwt

from app.config import settings
from app.users.auth import create_access_token
from app.users.dao import UsersDAO


def get_token(request: Request, token_name: str):
    """Функция, получающая токен из cookies по имени"""
    token = request.cookies.get(token_name)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Отсутствует токен: {token_name}"
        )
    return token


def get_access_token(request: Request) -> str:
    """Функция, возвращающая access токен"""
    return get_token(request, "todolist_access_token")


def get_refresh_token(request: Request) -> str:
    """Функция, возвращающая refresh токен"""
    return get_token(request, "todolist_refresh_token")


def decode_jwt(token: str):
    """Функция, декодирующая токен"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM, options={"verify_exp": False})
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена"
        )
    return payload


async def get_current_user(request: Request, response: Response):
    """Функция, получающая текущего авторизованного пользователя на основе access и refresh токенов из cookies."""
    access_token = get_access_token(request)
    refresh_token = get_refresh_token(request)
    
    payload = decode_jwt(access_token)

    if not payload or int(payload.get("exp", 0)) < datetime.now(timezone.utc).timestamp():
        try:
            refresh_payload = decode_jwt(refresh_token)
        except HTTPException:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходима повторная авторизация")
        if int(refresh_payload.get("exp", 0)) < datetime.now(timezone.utc).timestamp():
            raise HTTPException(status_code=401, detail="Refresh токен просрочен")
        
        user_id = refresh_payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Ошибка в refresh токене")
        
        new_access_token = create_access_token({"sub": user_id})
        response.set_cookie("todolist_access_token", new_access_token, httponly=True)
        payload = refresh_payload
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден пользователь"
        )

    return user

