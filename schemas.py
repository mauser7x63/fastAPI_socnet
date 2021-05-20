from typing import List, Optional
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    content: str
    author_id: int
    likes: int = 0
    dislikes: int = 0
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    content: str
    user_id: int
    token: str

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

class AuthModel(BaseModel):
    username: str
    password: str