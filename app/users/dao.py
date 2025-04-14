"""Модуль, описывающий слой работы с БД для таблицы пользователей"""

from app.dao.basedao import BaseDAO
from app.users.model import Users


class UsersDAO(BaseDAO):
    model = Users
