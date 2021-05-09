from typing import Optional
from pydantic import BaseModel


class Preview(BaseModel):
    width: Optional[int]
    height: Optional[int]
    url: Optional[str]
