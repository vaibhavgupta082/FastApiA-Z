from typing import List, Optional
from pydantic import BaseModel

class PromptRequest(BaseModel):
    Source: str
    Destination: str
    Days: str
    People: str
    Budget: str
    Month: str

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    blogs : List[Blog] =[]
    class Config():
        orm_mode = True

class UserCreate(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body:str
    creator: UserCreate

    class Config():
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
    class Config():
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None