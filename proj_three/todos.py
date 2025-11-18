from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 0
    due_date: Optional[datetime] = None
    id: Optional[int] = None
    user_id: Optional[int] = None
    is_completed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str