from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List
from ..database import get_db
from .. import hashing
from ..repository.User import get_all, create, get_by_id , delete, update

router = APIRouter(tags=["Users"], prefix="/user")


@router.post("/", response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return create(request, db)


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return get_by_id(db, id)


@router.get("/", response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(get_db)):
    return get_all(db)


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return delete(db, id)


@router.put("/{id}")
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return update(db, id, request)
