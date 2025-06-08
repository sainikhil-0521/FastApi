from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from .. import schemas, models, database, hashing
from ..controllers import user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=['User'])

@router.post('', status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = user.createUser(request, db)
    return {"data": {"message": "User created", "user": new_user.username}}

@router.get('/{user_id}', response_model=schemas.ShowUser)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    return user.getUserById(user_id, db)