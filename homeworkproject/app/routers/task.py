import asyncio
from slugify import slugify
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session, relationship
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateTask, UpdateTask, CreateUser
from app.models import User
from app.models import Task
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update

router2 = APIRouter(prefix='/task', tags=['task'])

@router2.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router2.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id:int):
    taskids = db.scalars(select(Task)).all()
    for i in taskids:
        if i.id == task_id:
            return i.title
    raise HTTPException(status_code=404, detail="Task was not found")

@router2.post("/create")
async def crate_task(db: Annotated[Session, Depends(get_db)], user_id:int, createtask: CreateTask):
    users = db.scalar(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(insert(Task).values
               (title=createtask.title,
                content=createtask.content,
                priority=createtask.priority,
                user_id=user_id,
                slug=slugify(createtask.title)
                ))
    db.commit()
    return {
        'status code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router2.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], updatetask: UpdateTask, task_id:int):
    taskid_for_update = db.scalar(select(User).where(Task.id == task_id))
    if taskid_for_update is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    db.execute(update(Task).where(Task.id == task_id).values
               (title=updatetask.title,
                content=updatetask.content,
                priority=updatetask.priority,
                slug=slugify(updatetask.title)

                ))
    db.commit()
    return {
        'status code': status.HTTP_201_CREATED,
        'transaction': 'Task update is successful!'
    }

@router2.delete("/delete")
async def delete_task(task_id:int, db: Annotated[Session, Depends(get_db)]):
    taskid_for_delete = db.scalar(select(Task).where(Task.id == task_id))
    if taskid_for_delete is None:
            raise HTTPException(status_code=404, detail="Task was not found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status code': status.HTTP_201_CREATED, 'transaction': 'Task was deleted!'}