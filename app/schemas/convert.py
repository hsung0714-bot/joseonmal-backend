from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ConvertRequest(BaseModel):
    original_text: str = Field(min_length=1, max_length=100)


class HighlightedWord(BaseModel):
    word: str
    modern: str
    position: list[int]


class ConvertResponse(BaseModel):
    converted_text: str
    highlighted_words: list[HighlightedWord]


class ConversionHistoryItem(BaseModel):
    id: UUID
    original_text: str
    converted_text: str
    created_at: datetime

    model_config = {"from_attributes": True}
