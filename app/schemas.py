from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Todo Schemas
class TodoBase(BaseModel):
    task: str
    completed: Optional[bool] = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    task: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    owner: User

    class Config:
        orm_mode = True