from .. import models
from sqlalchemy.orm import Session
from ..schemas import ShowBlog, Blog, BlogBase
from fastapi import HTTPException, status
from .. import hashing


def get_all(db: Session):
    users = db.query(models.User).all()
    return users

def create(request: Blog, db: Session):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_by_id(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user

def delete(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    user.delete(synchronize_session=False)
    db.commit()
    return "done"

def update(db: Session, id: int, request: Blog):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    user.update(
        {"name": request.name, "email": request.email, "password": request.password}
    )
    db.commit()
    db.refresh(user.first())
    return "updated"

