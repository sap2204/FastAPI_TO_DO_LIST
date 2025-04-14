# API-сервис для управления пользователями и задачами

Сервис предоставляет возможность создания, чтения, обновления и удаления (CRUD) пользователей и задач.  
Реализованы аутентификация и авторизация пользователей, а также написаны тесты для ключевых функций.

## 🛠️ Стек технологий

- Python  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Pytest  
- Docker + Docker Compose

## 🚀 Запуск приложения

### 1. Локальный запуск через Uvicorn

Убедитесь, что вы находитесь в корневой директории проекта, активировали виртуальное окружение и установите зависимости командойЖ

> poetry install

### 1.1 Настройка переменных окружения

Переименуйте файлы файлы:


> .env.example → .env  
> .env-non-dev.example → .env-non-dev

В указанных файлах замените **** на Ваши данные для подключения к базе данных.

### 1.2 Перед запуском приложения создайте таблицы пользователей и задач в БД, прогнав миграции командой:

> alembic upgrade head

1.3 Запустите приложение командой:

> uvicorn app.main:app --reload

После запуска приложение будет доступно по адресу:
> http://localhost:8000/docs

### 2. Сборка образа вручную через Docker

Если вы хотите собрать только образ приложения:

> docker build .

### 3. Запуск всех сервисов через Docker Compose
Если вы хотите запустить сразу всё (приложение FastAPI + базу данных):

> docker compose build

docker compose up

После запуска контейнеров документация API будет доступна по адресу:

> `http://localhost:9000/docs`


## Примеры запросов с использованием URL

Регистрация нового пользователя

curl -X 'POST' \
  'http://localhost:8000/users/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123"
}'

Вход пользователя

curl -X 'POST' \
  'http://localhost:8000/users/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "john.doe@example.com",
  "password": "password123"
}'

Получение списка всех пользователей

curl -X 'GET' \
  'http://localhost:8000/users/all_users'

Получение информации о пользователе по ID

curl -X 'GET' \
  'http://localhost:8000/users/1'

Выход из аккаунта

curl -X 'POST' \
  'http://localhost:8000/users/logout'

Добавление задачи

curl -X 'POST' \
  'http://localhost:8000/tasks/add_task' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Finish the project",
  "description": "Complete the FastAPI application",
  "status": "In Progress"
}'

Получение списка всех задач

curl -X 'GET' \
  'http://localhost:8000/tasks/all_tasks'

Получение задачи по ID

curl -X 'GET' \
  'http://localhost:8000/tasks/1'

Обновление задачи

curl -X 'PUT' \
  'http://localhost:8000/tasks/update/1' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Finish the project with tests",
  "description": "Complete the FastAPI application with unit tests",
  "status": "In Progress"
}'

Удаление задачи

curl -X 'DELETE' \
  'http://localhost:8000/tasks/delete/1'

📌 Описание работы с токенами и куки
При входе в аккаунт с помощью эндпоинта /users/login, сервер генерирует токен доступа и отправляет его как cookie (todolist_access_token).

Этот токен должен быть передан в запросах для авторизации, если они требуют аутентификации. Для этого достаточно, чтобы браузер или клиент отправлял его в cookie.

Пример: Установка токена в cookie

curl -X 'POST' \
  'http://localhost:8000/users/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "john.doe@example.com",
  "password": "password123"
}' -c cookies.txt
Когда вы выходите из аккаунта с помощью эндпоинта /users/logout, токен удаляется из cookie, и дальнейшие запросы без токена будут отклоняться.

Пример: Удаление токена

curl -X 'POST' \
  'http://localhost:8000/users/logout' \
  -b cookies.txt