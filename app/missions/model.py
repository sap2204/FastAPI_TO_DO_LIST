"""Модуль, описывающий таблицу задач"""

import enum

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MissionStatus(enum.Enum):
    """Класс, описывающий возможные состояния задач"""

    new = "new"
    in_progress = "in_progress"
    completed = "completed"


class Missions(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[MissionStatus] = mapped_column(Enum(MissionStatus), nullable=False)
