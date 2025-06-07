from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Optional
from pydantic import BaseModel
from . import schemas, models, database
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)
@app.get("/")
def index():
    return {"data": {"message": "Blog List"}}
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(blog_post: schemas.BlogPost, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(
        title=blog_post.title,
        content=blog_post.content,
        published=blog_post.published
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": {"message": "Blog created", "blog": new_blog.title}}

@app.get("/blog")
def get_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return {"data": blogs}

@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def get_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return {"data": {"id": blog.id, "title": blog.title, "content": blog.content, "published": blog.published}}

@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/blog/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, blog_post: schemas.BlogPost, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    blog.title = blog_post.title
    blog.content = blog_post.content
    blog.published = blog_post.published
    
    db.commit()
    db.refresh(blog)
    
    return {"data": {"message": "Blog updated", "blog": blog.title}}