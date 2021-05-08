from typing import Optional
from pydantic import BaseModel


class Thumbnails(BaseModel):
    web: Optional[str]
    web_large: Optional[str]
    mobile: Optional[str]
    tablet: Optional[str]
