from typing import Optional
from pydantic import BaseModel

class BlogPost(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    created_at: str