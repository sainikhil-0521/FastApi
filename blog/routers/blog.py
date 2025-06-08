from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session
from ..controllers import blog

router = APIRouter(prefix="/blog", tags=["Blog"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_blog(blog_post: schemas.BlogPost, db: Session = Depends(database.get_db)):
    new_blog = blog.createBlog(blog_post, db)
    return {"data": {"message": "Blog created", "blog": new_blog.title}}

@router.get("", response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(database.get_db)):
    blogs = blog.getBlogs(db)
    return blogs

@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blogRecord = blog.getBlogById(blog_id, db)
    if blogRecord is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blogRecord

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
    return blog.deleteBlog(blog_id, db)

@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, blog_post: schemas.BlogPost, db: Session = Depends(database.get_db)):
    blog = blog.updateBlog(blog_id, blog_post, db)
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return {"data": {"message": "Blog updated", "blog": blog.title}}
