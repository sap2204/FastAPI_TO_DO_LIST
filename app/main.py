from fastapi import FastAPI

from app.missions.router import router as tasks_router
from app.users.router import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)
