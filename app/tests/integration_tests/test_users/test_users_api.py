"""Модуль, описывающий интеграционные тесты API пользователей"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, email, password, status",
    [
        ("sergei", "sergei@sergei.com", "sergei", 201),
        ("sergei", "sergei@sergei.com", "sergei", 409),
        ("sergei", "wrong_email", "sergei", 422),
    ],
)
async def test_add_user(name, email, password, status, async_client: AsyncClient):
    """Тест на добавление нового пользователя"""
    response = await async_client.post(
        "/users/register", json={"name": name, "email": email, "password": password}
    )

    assert response.status_code == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email, password, status",
    [
        ("test1@test1.com", "test", 200),
        ("test2@test2.com", "artem", 200),
        ("test@test1.com", "test", 401),
        ("test1@test1.com", "test_1", 401),
    ],
)
async def test_login_user(email, password, status, async_client: AsyncClient):
    """Тест, проверяющий вход в аккаунт"""
    response = await async_client.post(
        "/users/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status


@pytest.mark.asyncio
async def test_logout_user(async_client: AsyncClient):
    """Тест, проверяющий выход из аккаунта"""
    response = await async_client.post("users/logout")
    assert response.status_code == 204
    assert "todolist_access_token" not in async_client.cookies


@pytest.mark.asyncio
async def test_get_all_users(async_client: AsyncClient):
    """Тест, проверяющий получение всех пользователей"""
    response = await async_client.get("users/all_users")
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, status", [(1, 200), (2, 200), (10, 404)])
async def test_get_user_by_id(user_id, status, async_client: AsyncClient):
    """Тест, проверяющий получение пользователя по id"""
    response = await async_client.get(f"users/{user_id}")
    if user_id in [1, 2]:
        assert response.status_code == status
        assert response.json()["email"] in ["test1@test1.com", "test2@test2.com"]
    else:
        assert response.status_code == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, name, email, password, status",
    [
        (1, "test3", "test3@test3.com", "test3", 200),
        (10, "test2", "test2@test2.com", "test", 404),
        (1, "test2", "email", "test", 422),
    ],
)
async def test_update_user_by_id(
    user_id, name, email, password, status, async_client: AsyncClient
):
    """Тест, реализующий проверку обновления пользователя"""
    response = await async_client.put(
        f"users/update/{user_id}",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status
    if response.status_code == 200:
        assert response.json()["id"] == user_id
        assert response.json()["name"] == name
        assert response.json()["email"] == email


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id, status", [(1, 204), (2, 204), (10, 404)])
async def test_delete_user_by_id(user_id, status, async_client: AsyncClient):
    """Тест, проверяющий удаление пользователя по id"""
    response = await async_client.delete(f"users/delete/{user_id}")
    assert response.status_code == status
