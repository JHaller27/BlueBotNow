from typing import Optional, List
from .thumbnails import Thumbnails
from .descriptionPanel import DescriptionPanel
from .chatSettings import ChatSettings
from .multistreamItem import MultistreamItem
from .language import Language
from pydantic import BaseModel


class ChannelDetails(BaseModel):
    account_type: Optional[str]
    adult: Optional[bool]
    avatar: Optional[str]
    category: Optional[List[str]]
    chat_settings: Optional[ChatSettings]
    commissions: Optional[bool]
    creation_date: Optional[str]
    description_panels: Optional[List[DescriptionPanel]]
    followers: Optional[int]
    following: Optional[bool]
    gaming: Optional[bool]
    languages: Optional[List[Language]]
    last_live: Optional[str]
    multistream: Optional[List[MultistreamItem]]
    name: Optional[str]
    online: Optional[bool]
    private: Optional[bool]
    private_message: Optional[str]
    recordings: Optional[bool]
    subscribers: Optional[int]
    tags: Optional[List[str]]
    thumbnails: Optional[Thumbnails]
    title: Optional[str]
    user_id: Optional[int]
    viewers: Optional[int]
    viewers_total: Optional[int]
