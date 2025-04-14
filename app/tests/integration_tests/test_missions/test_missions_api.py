"""Модуль, описывающие интеграционные тесты API задач"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description, status, status_code",
    [
        ("task_5", "d_task_5", "new", 201),
        ("task_6", "d_task_6", "in_progress", 201),
        ("task_7", "d_task_8", "completed", 201),
        ("task_7", "d_task_8", "something", 422),
    ],
)
async def test_add_new_task(
    name, description, status, status_code, authenticated_ac: AsyncClient
):
    """Тест, проверяющий добавление новой задачи авторизованным пользователем"""
    response = await authenticated_ac.post(
        "/tasks/add_task",
        json={"name": name, "description": description, "status": status},
    )
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_get_all_tasks(async_client: AsyncClient):
    """Тест, проверяющий получение всех задач"""
    response = await async_client.get("/tasks/all_tasks")
    assert response.status_code == 200
    assert len(response.json()) == 7


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_id, status", [(1, 200), (4, 200), (0, 404), (100, 404), (-1, 404)]
)
async def test_get_task_by_id(task_id, status, async_client: AsyncClient):
    """Тест, проверяющий получение задачи по ее id"""
    response = await async_client.get(f"/tasks/{task_id}")
    assert response.status_code == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_id, name, description, status, status_code",
    [
        (1, "task_0", "d_task_0", "new", 200),
        ("one", "task_0", "d_task_0", "new", 422),
        (100, "task_0", "d_task_0", "new", 404),
    ],
)
async def test_update_task_by_id(
    task_id, name, description, status, status_code, authenticated_ac: AsyncClient
):
    """Тест, проверяющий обновление задачи авторизованным пользователем"""
    response = await authenticated_ac.put(
        f"tasks/update/{task_id}",
        json={"name": name, "description": description, "status": status},
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        assert response.json()["id"] == task_id
        assert response.json()["name"] == name
        assert response.json()["description"] == description
        assert response.json()["status"] == status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_id, status",
    [
        (1, 204),
        (3, 204),
        (100, 404),
        (-1, 404),
    ],
)
async def test_delete_task_by_id(task_id, status, authenticated_ac: AsyncClient):
    """Тест, проверяющий удаление задачи по ее id авторизованным пользователем"""
    response = await authenticated_ac.delete(f"tasks/delete/{task_id}")
    assert response.status_code == status
