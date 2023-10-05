from pydantic import BaseModel
from datetime import datetime
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

    class Config:
        orm_mode = True
