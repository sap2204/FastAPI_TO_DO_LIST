"""Модуль, описывающий эндпоинты задач"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.missions.dao import MissionsDAO
from app.missions.schemas import SMission, SMissionAdd
from app.users.dependencies import get_current_user
from app.users.schemas import SUser

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post("/add_task", status_code=201)
async def add_new_task(
    task_data: SMissionAdd, current_user: SUser = Depends(get_current_user)
):
    """Функция, реализующая добавление новой записи"""
    new_task = task_data.model_dump()
    new_task["user_id"] = current_user.id
    await MissionsDAO.add_to_db(**new_task)
    return {"message": f"Задача '{task_data.name}' добавлена"}


@router.get("/all_tasks", status_code=200)
async def get_all_tasks() -> list[SMission]:
    """Функция, возвращающая список всех задач"""
    tasks = await MissionsDAO.find_all()
    return tasks


@router.get("/{task_id}", status_code=200)
async def get_task_by_id(task_id: int) -> SMission:
    """Функция, возвращающая задачу по id задачи"""
    existing_task = await MissionsDAO.find_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id = {task_id} не найдена",
        )
    return existing_task


@router.put("/update/{task_id}", status_code=200)
async def update_task_by_id(
    task_id: int,
    task_data: SMissionAdd,
    current_user: SUser = Depends(get_current_user),
):
    """Функция, реализующая обновление задачи"""
    existing_task = await MissionsDAO.find_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id = {task_id} не найдена",
        )
    new_task = task_data.model_dump()
    new_task["user_id"] = current_user.id
    updated_task = await MissionsDAO.update(task_id, new_task)
    return {
        "id": updated_task.id,
        "name": updated_task.name,
        "description": updated_task.description,
        "status": updated_task.status,
    }


@router.delete("/delete/{task_id}", status_code=204)
async def delete_task_by_id(
    task_id: int, current_user: SUser = Depends(get_current_user)
):
    """Функция, реализующая удаление задачи"""
    existing_task = await MissionsDAO.find_by_id(task_id)
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id = {task_id} не найдена",
        )
    await MissionsDAO.delete(id=task_id)
    return {"message": f"Задача с id = {task_id} удалена"}
