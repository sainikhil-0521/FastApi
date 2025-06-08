from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from . import schemas, models, database, hashing
from sqlalchemy.orm import Session
from .routers import blog, user, authentication

app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

models.Base.metadata.create_all(bind=database.engine)
@app.get("/")
def index():
    return {"data": {"message": "Blog List"}}
