"""Модуль, описывающий слой работы с БД для таблицы задачи"""

from app.dao.basedao import BaseDAO
from app.missions.model import Missions


class MissionsDAO(BaseDAO):
    model = Missions
