from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session

def createUser(user: schemas.User, db: Session = Depends(database.get_db)):
    hashedPassword = hashing.Hash().hash(user.password)
    new_user = models.User(username=user.username, password=hashedPassword, email=user.email, created_at=user.created_at)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def getUserById(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user