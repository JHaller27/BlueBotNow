from typing import Optional
from pydantic import BaseModel


class Score(BaseModel):
    up: Optional[int]
    down: Optional[int]
    total: Optional[int]
