from typing import Any, Optional, List
from .file import File
from .preview import Preview
from .sample import Sample
from .score import Score
from .tags import Tags
from .flags import Flags
from .relationships import Relationships
from pydantic import BaseModel


class Post(BaseModel):
    id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    file: Optional[File]
    preview: Optional[Preview]
    sample: Optional[Sample]
    score: Optional[Score]
    tags: Optional[Tags]
    locked_tags: Optional[Any]
    change_seq: Optional[int]
    flags: Optional[Flags]
    rating: Optional[str]
    fav_count: Optional[int]
    sources: Optional[List[str]]
    pools: Optional[Any]
    relationships: Optional[Relationships]
    approver_id: Optional[int]
    uploader_id: Optional[int]
    description: Optional[str]
    comment_count: Optional[int]
    is_favorited: Optional[bool]
    has_notes: Optional[bool]
    duration: Optional[None]
