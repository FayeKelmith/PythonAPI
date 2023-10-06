from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Pydantic model for creating user:

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Pydantic model for response to user


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

# pydantic schema to handle request structure


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

# AIM: to have granully control


class PostCreate(PostBase):
    pass


# PYdantic for response

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        from_attributes = True
