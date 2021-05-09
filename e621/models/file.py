from typing import Optional
from pydantic import BaseModel


class File(BaseModel):
    width: Optional[int]
    height: Optional[int]
    ext: Optional[str]
    size: Optional[int]
    md5: Optional[str]
    url: Optional[str]
