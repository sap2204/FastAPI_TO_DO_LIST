"""Модуль, описывющий схемы входных и выходных данных для пользователей"""

from pydantic import BaseModel, EmailStr


class SUser(BaseModel):
    """Класс, описывающий модель возврата пользователя"""

    email: EmailStr
    password: str


class SUserAuth(BaseModel):
    """Класс, описывающий схему данных при регистрации нового пользователя
    и входа в аккаунт"""

    name: str
    email: EmailStr
    password: str
