from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime  # Assuming created_at is a string, adjust as necessary
    class Config:
        from_attributes = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    post_id: int
    created_at: datetime
    votes: int = 0  # Assuming votes is an integer count of votes
    owner: UserResponse
    class Config:
        from_attributes = True  # This allows Pydantic to read data from ORM models


class Vote(BaseModel):
    post_id: int
    dir: int  # 1 for like, 0 for unlike