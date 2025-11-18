
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

router  = APIRouter()

@router.get("/users", response_model=List[UserSchema], tags=["Users"])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=UserSchema, tags=["Users"])
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_with_db)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None

