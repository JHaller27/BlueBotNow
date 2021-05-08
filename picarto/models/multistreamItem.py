from typing import Optional
from pydantic import BaseModel


class MultistreamItem(BaseModel):
    user_id: Optional[int]
    name: Optional[str]
    online: Optional[bool]
    adult: Optional[bool]
