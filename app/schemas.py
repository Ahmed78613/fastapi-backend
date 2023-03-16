from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


#! User
# Request Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Response Schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    # Will Read Even When Not A dictionary
    class Config:
        orm_mode = True


#! Post
# Base Schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # Default


# Request Schema (Extends PostBase)
class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # Will Read Even When Not A dictionary
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    # Will Read Even When Not A dictionary
    class Config:
        orm_mode = True


# Response Schema (Extends PostBase)
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    # Will Read Even When Not A dictionary
    class Config:
        orm_mode = True


#! Auth
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


#! Vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # Anything <= 1
