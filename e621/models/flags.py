from typing import Optional
from pydantic import BaseModel


class Flags(BaseModel):
    pending: Optional[bool]
    flagged: Optional[bool]
    note_locked: Optional[bool]
    status_locked: Optional[bool]
    rating_locked: Optional[bool]
    deleted: Optional[bool]
