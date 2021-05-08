from typing import Optional
from pydantic import BaseModel


class ChatSettings(BaseModel):
    guest_chat: Optional[bool]
    links: Optional[bool]
    level: Optional[bool]
