from pydantic import BaseModel
from typing import List


class PreferenceUpdate(BaseModel):
    country: str
    state: str
    language: str
    voice: str
    categories: List[str]
    duration: int


class PodcastGenerateRequest(BaseModel):
    user_id: int = 1