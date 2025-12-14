from .. import models
from sqlalchemy.orm import Session
from ..schemas import ShowBlog, Blog, BlogBase , User
from fastapi import HTTPException, status
from fastapi import Depends
from . User import get_by_email


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request :Blog, db: Session , current_user : User):
    print(f"Creating blog for user: {current_user}")
    user_id = get_by_email(db, current_user.email)  # Ensure user exists
    print(f"user_id: {user_id.id}")
    new_blog = models.Blog(title=request.title, body=request.body , user_id=user_id.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def get_by_id(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    return blog

def delete(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return "done"

def update(db: Session, id: int, request: Blog):
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