from typing import Optional, Any
from pydantic import BaseModel


class Sample(BaseModel):
    has: Optional[bool]
    height: Optional[int]
    width: Optional[int]
    url: Optional[str]
    alternates: Optional[Any]
