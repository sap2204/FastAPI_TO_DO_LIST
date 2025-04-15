"""Модуль для подготовки тестовой БД и наполнение ее тестовыми данными"""

import json

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.missions.model import Missions
from app.users.model import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Фикстура, подготавливающая тестовую БД"""
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        """Функция, открывающая файлы с тестовыми данными"""
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    missions = open_mock_json("missions")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)
        add_missions = insert(Missions).values(missions)

        await session.execute(add_users)
        await session.execute(add_missions)

        await session.commit()


@pytest.fixture(scope="function")
async def async_client():
    """Фикстура, создающая асинхронного клиента для тестов"""
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="session")
async def authenticated_ac():
    """Фикстура, создающая аутентифицированного пользователя"""
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        await async_client.post(
            "users/login", json={"email": "test1@test1.com", "password": "test1"}
        )
        assert async_client.cookies["todolist_access_token"]
        yield async_client
