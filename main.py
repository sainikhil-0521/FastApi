from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True  
@app.get("/")
def index():
    return {"data": {"message": "Blog List"}}

@app.get("/blog")
def get_blog(limit: int = 10, skip:int = 0, unpublished: bool = False, sort: Optional[str]= None):
    if unpublished:
        return {"data": "Unpublished blogs"}
    return {"data": f"Blogs with limit {limit} and skip {skip}"}


@app.get("/blog/{id}")
def get_blog(id: int):
    return {"data": {"blog_id": id}}

@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"Blog created with title: {blog.title}"}

