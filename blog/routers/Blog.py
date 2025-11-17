from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database import get_db
from ..schemas import ShowBlog, Blog, BlogBase
from .. import models
from sqlalchemy.orm import Session
from .. repository.Blog import get_all, create, get_by_id, delete , update


router = APIRouter(tags=["Blogs"], prefix="/blog")


@router.get("/blog", response_model=List[ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    return get_all(db)


@router.get("/{id}", response_model=ShowBlog)
def blog(id: int, db: Session = Depends(get_db)):
    return get_by_id(db, id)



@router.post("/", response_model=BlogBase)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    return create(request, db)


@router.delete("/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):
    return delete(db, id)


@router.put("/{id}")
def update_blog(id: int, request: Blog, db: Session = Depends(get_db)):
    return update(db, id, request)
