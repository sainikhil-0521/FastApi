from typing import Optional, List
from pydantic import BaseModel

class BlogPost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    user_id: int

class User(BaseModel):
    username: str
    email: str
    password: str
    created_at: str

class ShowBlogInUser(BaseModel):
    title: str
    content: str
    published: bool
    class Config:
        orm_mode = True
class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[ShowBlogInUser]
    class Config:
        orm_mode = True
        
class ShowUserInBlog(BaseModel):
    username: str
    email: str
    
class ShowBlog(BaseModel):
    title: str
    published: bool
    creator: ShowUserInBlog
    
class UserLogin(BaseModel):
    username: str
    password: str
