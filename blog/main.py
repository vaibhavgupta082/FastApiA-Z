from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, database
from typing import List
from . import hashing
from .database import get_db
from .routers import Blog, User, authentication


models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

app.include_router(authentication.router)
app.include_router(Blog.router)
app.include_router(User.router)
