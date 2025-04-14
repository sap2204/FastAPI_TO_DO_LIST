"""Модуль, описывающий входные и выходные схемы задач"""

from pydantic import BaseModel

from app.missions.model import MissionStatus


class SMissionAdd(BaseModel):
    """Класс, реализующий схему добавления новой задачи"""

    name: str
    description: str
    status: MissionStatus

    class Config:
        use_enum_values = True


class SMission(BaseModel):
    """Класс, описывающий схему задачи"""

    id: int
    user_id: int
    name: str
    description: str
    status: str
