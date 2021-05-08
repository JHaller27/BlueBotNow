from typing import Optional
from pydantic import BaseModel


class Language(BaseModel):
    id: Optional[int]
    name: Optional[str]
