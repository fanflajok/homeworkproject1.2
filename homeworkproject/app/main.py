from fastapi import FastAPI
from routers import user
from routers import task
from app.backend.db_depends import get_db
import asyncio


fapp = FastAPI()
fapp.include_router(user.router1)
fapp.include_router(task.router2)

greeting = {'message': 'Welcome to Taskmanager'}


@fapp.get("/")
async def welcome_def():
    return greeting


