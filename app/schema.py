from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

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


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        from_attributes = True
