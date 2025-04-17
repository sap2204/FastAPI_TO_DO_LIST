"""Модуль описывает создание приложения FastAPI и подключения к нему роутеров
с пользователями и с задачами. Подключает логирование через мидлвари
и перехватчик исключений в эндпоинтах.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger

from app.missions.router import router as tasks_router
from app.users.router import router as users_router

app = FastAPI()

logger.add(
    "app/logs/logs.json",
    format="{time} -> {level} -> {message}",
    level="INFO",
    rotation="10 Mb",
    compression="zip",
    serialize=True,
)


@app.middleware("http")
async def log_endponts(request: Request, call_text):
    """Функция, реализующая логирование эндпоинтов"""
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_text(request)
    logger.info(f"Response: {response.status_code}")
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exception: HTTPException):
    """Функция, реализующая перехват ошибок в эндпоинтах"""
    logger.error(f"Error: {exception.detail} on {request.url}")
    return JSONResponse(
        status_code=exception.status_code, content={"message": exception.detail}
    )


app.include_router(users_router)
app.include_router(tasks_router)
