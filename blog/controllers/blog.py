from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from .. import schemas, models, database, hashing
from sqlalchemy.orm import Session

def createBlog(blog_post: schemas.BlogPost, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(
        title=blog_post.title,
        content=blog_post.content,
        published=blog_post.published,
        user_id=blog_post.user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def getBlogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

def getBlogById(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        return None
    return blog

def deleteBlog(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def updateBlog(blog_id: int, blog_post: schemas.BlogPost, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    blog.title = blog_post.title
    blog.content = blog_post.content
    blog.published = blog_post.published
    
    db.commit()
    db.refresh(blog)
    return blog