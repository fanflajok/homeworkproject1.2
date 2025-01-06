import asyncio
from slugify import slugify
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateUser, UpdateUser
from app.models import User
from app.models import Task
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy import update




router1 = APIRouter(prefix='/user', tags=['user'])

@router1.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router1.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id:int):
    uids = db.scalars(select(User)).all()
    for i in uids:
        if i.id == user_id:
            return i.username
    raise HTTPException(status_code=404, detail="User was not found")
@router1.post("/create")
async def create_user(create: CreateUser, db: Annotated[Session, Depends(get_db)]):
    usernames = db.scalars(select(User.username)).all()
    for i in usernames:
        if i == create.username:
            raise HTTPException(status_code=404, detail="User already exists")
    db.execute(insert(User).values(username=create.username,
                                   firstname=create.firstname,
                                   lastname=create.lastname,
                                   age=create.age,
                                   slug=slugify(create.username)
    ))
    db.commit()
    return {
        'status code': status.HTTP_201_CREATED,
        'transaction': 'Successful'

    }
@router1.put("/update")
async def update_user(updateuser: UpdateUser, user_id:int, db: Annotated[Session, Depends(get_db)]):
    userid_for_update = db.scalar(select(User).where(User.id == user_id))
    if userid_for_update is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(update(User).where(User.id == user_id).values
                                    (username=updateuser.username,
                                   firstname=updateuser.firstname,
                                   lastname=updateuser.lastname,
                                   age=updateuser.age,
                                    slug=slugify(updateuser.username)

            ))
    db.commit()
    return {
                'status code': status.HTTP_201_CREATED,
                'transaction': 'User update is successful!'
            }

@router1.delete("/delete")
async def delete_user(user_id:int, db: Annotated[Session, Depends(get_db)]):
    userid_for_delete = db.scalar(select(User).where(User.id == user_id))
    if userid_for_delete is None:
            raise HTTPException(status_code=404, detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {'status code': status.HTTP_201_CREATED, 'transaction': 'User and his tasks were deleted!'}


@router1.get("/user_id/tasks" )
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id:int):
    tasks_by_users_id = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks_by_users_id
