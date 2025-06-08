from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session
from ..controllers import blog

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not hashing.Hash().verify(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"message": "Login successful", "user": db_user.username}