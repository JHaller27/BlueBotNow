from typing import Any, Optional, List
from pydantic import BaseModel


class Tags(BaseModel):
    general: Optional[List[str]]
    species: Optional[List[str]]
    character: Optional[List[str]]
    copyright: Optional[Any]
    artist: Optional[List[str]]
    invalid: Optional[Any]
    lore: Optional[Any]
    meta: Optional[List[str]]
