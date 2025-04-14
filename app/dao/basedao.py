"""Модуль, описывающий операции CRUD с БД"""

from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker


class BaseDAO:
    """Класс, описывающий операции CRUD"""

    model = None

    @classmethod
    async def find_all(cls):
        """Метод, позволяющий получить все записи из БД в зависимости от модели"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, **filter):
        """Метод, возвращающий либо одну запись из БД, либо ничего"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        """Метод, позволяющий найти запись по id"""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def add_to_db(cls, **data):
        """Метод, описывающий добавление записи в БД"""
        async with async_session_maker() as session:
            statement = insert(cls.model).values(**data)
            await session.execute(statement)
            await session.commit()

    @classmethod
    async def update(cls, model_id: int, data: dict):
        """Метод, описывающий обновление записи в БД по id"""
        async with async_session_maker() as session:
            statement = update(cls.model).where(cls.model.id == model_id).values(**data)
            await session.execute(statement)
            await session.commit()

            stmt = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(stmt)
            updated_user = result.scalar_one_or_none()
            return updated_user

    @classmethod
    async def delete(cls, **filter):
        """Метод, описывающий удаление записи из БД"""
        async with async_session_maker() as session:
            statement = delete(cls.model).filter_by(**filter)
            await session.execute(statement)
            await session.commit()
