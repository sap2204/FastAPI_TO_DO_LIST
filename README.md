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
- Loguru

## 🚀 Запуск приложения

### 1. Локальный запуск через Uvicorn

Убедитесь, что вы находитесь в корневой директории проекта, активировали виртуальное окружение и установите зависимости командой:

> poetry install

### 1.1 Настройка переменных окружения ⚙️

Переименуйте файлы файлы:


> .env.example → .env  
> .env-non-dev.example → .env-non-dev

В указанных файлах введите Ваши данные для подключения к базе данных.

### 1.2 Перед запуском приложения создайте таблицы пользователей и задач в БД, прогнав миграции командой 🛠️:

> alembic upgrade head

1.3 Запустите приложение командой:

> uvicorn app.main:app --reload

После запуска приложение будет доступно по адресу:
> http://localhost:8000/docs

### 2. Сборка образа вручную через Docker 🐳

Если вы хотите собрать только образ приложения:

> docker build .

### 3. Запуск всех сервисов через Docker Compose 🐋📦
Если вы хотите запустить сразу всё (приложение FastAPI + базу данных):

> docker compose build

docker compose up

После запуска контейнеров документация API будет доступна по адресу:

> `http://localhost:9000/docs`


## Примеры запросов с использованием URL 🖥️

__Регистрация нового пользователя__

> curl -X 'POST' \
  'http://localhost:8000/users/register' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123"
}'

__Вход пользователя__

> curl -X 'POST' \
  'http://localhost:8000/users/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "john.doe@example.com",
  "password": "password123"
}'

__Получение списка всех пользователей__

> curl -X 'GET' \
  'http://localhost:8000/users/all_users'


__Получение информации о пользователе по ID__

> curl -X 'GET' \
  'http://localhost:8000/users/1'

__Выход из аккаунта__

> curl -X 'POST' \
  'http://localhost:8000/users/logout'

__Добавление задачи__

> curl -X 'POST' \
  'http://localhost:8000/tasks/add_task' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Finish the project",
  "description": "Complete the FastAPI application",
  "status": "In Progress"
}'

__Получение списка всех задач__

> curl -X 'GET' \
  'http://localhost:8000/tasks/all_tasks'

__Получение задачи по ID__

> curl -X 'GET' \
  'http://localhost:8000/tasks/1'

__Обновление задачи__

> curl -X 'PUT' \
  'http://localhost:8000/tasks/update/1' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Finish the project with tests",
  "description": "Complete the FastAPI application with unit tests",
  "status": "In Progress"
}'

__Удаление задачи__

> curl -X 'DELETE' \
  'http://localhost:8000/tasks/delete/1'

📌 Описание работы с токенами и куки.

При входе в аккаунт с помощью эндпоинта /users/login, сервер генерирует токен доступа (access token) и refresh token, отправляет их как cookie (todolist_access_token, todolist_refresh_token).

Этот access token должен быть передан в запросах для авторизации, если они требуют аутентификации. Для этого достаточно, чтобы браузер или клиент отправлял его в cookie.

__Пример: Установка токена в cookie__

> curl -X 'POST' \
  'http://localhost:8000/users/login' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "john.doe@example.com",
  "password": "password123"
}' -c cookies.txt

Когда вы выходите из аккаунта с помощью эндпоинта /users/logout, токен удаляется из cookie, и дальнейшие запросы без токена будут отклоняться.

__Пример: Удаление токена__

> curl -X 'POST' \
  'http://localhost:8000/users/logout' \
  -b cookies.txt


## 📋 Логирование

В проекте используется библиотека loguru для логирования.

Логи сохраняются в файл  __app/logs/logs.json__ в формате JSON.

__Файл логов автоматически:__

- ротацируется при достижении 10 MB;

- сжимается в .zip;

- содержит всю информацию о запросах, ответах, ошибках и вспомогательных функциях.
