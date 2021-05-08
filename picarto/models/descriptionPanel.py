from typing import Optional
from pydantic import BaseModel


class DescriptionPanel(BaseModel):
    title: Optional[str]
    body: Optional[str]
    image: Optional[str]
    image_link: Optional[str]
    button_text: Optional[str]
    button_link: Optional[str]
    position: Optional[int]
