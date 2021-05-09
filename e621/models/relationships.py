from typing import Any, Optional
from pydantic import BaseModel


class Relationships(BaseModel):
    parent_id: Optional[int]
    has_children: Optional[bool]
    has_active_children: Optional[bool]
    children: Optional[Any]
