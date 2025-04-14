"""Модуль, описывающий эндпоинты пользователей"""

from fastapi import APIRouter, HTTPException, Response, status

from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import SUser, SUserAuth

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/register", status_code=201)
async def add_user(user_data: SUserAuth):
    """Функция, реализующая добавление нового пользователя"""
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким email уже существует",
        )
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add_to_db(
        name=user_data.name, email=user_data.email, password=hashed_password
    )
    return {"message": f"Пользователь {user_data.name} с {user_data.email} добавлен"}


@router.post("/login", status_code=200)
async def login_user(response: Response, user_data: SUser):
    """Функция, реализующая вход в аккаунт"""
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не аутентифицирован",
        )
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("todolist_access_token", access_token, httponly=True)
    return {"message": "Вы успешно вошли в свой аккаунт"}


@router.post("/logout", status_code=204)
async def logout_user(response: Response):
    """Функция, реализующая выход из аккаунта"""
    response.delete_cookie("todolist_access_token")
    return {"message": "Вы вышли из аккаунта"}


@router.get("/all_users", status_code=200)
async def get_all_users() -> list[SUser]:
    """Функция, возращающая список пользователей"""
    users = await UsersDAO.find_all()
    return users


@router.get("/{user_id}", status_code=200)
async def get_user_by_id(user_id: int) -> SUser:
    """Функция, возвращающая пользователя по id"""
    user = await UsersDAO.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с id = {user_id} не существует",
        )
    return user


@router.put("/update/{user_id}", status_code=200)
async def update_user_by_id(user_id: int, user_data: SUserAuth):
    """Функция, обновляющая пользователя"""
    existing_user = await UsersDAO.find_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с id = {user_id} не существует",
        )
    updated_user = await UsersDAO.update(user_id, user_data.model_dump())
    return {
        "id": updated_user.id,
        "name": updated_user.name,
        "email": updated_user.email,
    }


@router.delete("/delete/{user_id}", status_code=204)
async def delete_user_by_id(user_id: int):
    """Функция, удаляющая пользователя по id"""
    existing_user = await UsersDAO.find_by_id(user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с id = {user_id} не существует",
        )
    await UsersDAO.delete(id=user_id)
    return {"message": f"Пользователь с id = {user_id} удален"}
