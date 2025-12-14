from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database import get_db
from ..schemas import ShowBlog, Blog, BlogBase , User
from .. import models
from sqlalchemy.orm import Session
from .. repository.Blog import get_all, create, get_by_id, delete , update
from .. import Oauth2


router = APIRouter(tags=["Blogs"], prefix="/blog")


@router.get("/blog", response_model=List[ShowBlog])
def all_blogs(db: Session = Depends(get_db) , current_user : User = Depends(Oauth2.get_current_user)):
    return get_all(db)


@router.get("/{id}", response_model=ShowBlog)
def blog(id: int, db: Session = Depends(get_db), current_user : User = Depends(Oauth2.get_current_user)):
    return get_by_id(db, id)



@router.post("/", response_model=BlogBase)
def create_blog(request: Blog, db: Session = Depends(get_db), current_user : User = Depends(Oauth2.get_current_user)):
    return create(request, db,current_user)


@router.delete("/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user : User = Depends(Oauth2.get_current_user)):
    return delete(db, id)


@router.put("/{id}")
def update_blog(id: int, request: Blog, db: Session = Depends(get_db), current_user : User = Depends(Oauth2.get_current_user)):
    return update(db, id, request)
