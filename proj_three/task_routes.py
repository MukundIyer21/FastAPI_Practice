
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from classes import User, Task
from todos import UserSchema, TaskSchema, Token
from auth import *

@router.post("/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(
    task: TaskSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    db_task = Task(
        user_id=current_user.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[TaskSchema], tags=["Tasks"])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    if completed is not None:
        query = query.filter(Task.is_completed == completed)
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskSchema, tags=["Tasks"])
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskSchema, tags=["Tasks"])
def update_task(
    task_id: int,
    task_update: TaskSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
 
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.patch("/tasks/{task_id}/complete", response_model=TaskSchema, tags=["Tasks"])
def mark_task_complete(
    task_id: int,
    is_completed: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_completed = is_completed
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return None