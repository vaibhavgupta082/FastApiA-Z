from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..database import get_db
from ..schemas import ShowBlog, Blog, BlogBase
from .. import models
from sqlalchemy.orm import Session


router = APIRouter(tags=["Blogs"], prefix="/blog")


@router.get("/blog", response_model=List[ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", response_model=ShowBlog)
def blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    return blog


@router.post("/", response_model=BlogBase)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@router.put("/{id}")
def update_blog(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    db.refresh(blog.first())
    return "updated"
