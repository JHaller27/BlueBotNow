from typing import Optional, List
from .post import Post
from pydantic import BaseModel


class Posts(BaseModel):
    posts: Optional[List[Post]]
