from uuid import UUID
from datetime import date
from pydantic import BaseModel


class DictionaryItem(BaseModel):
    id: UUID
    word: str
    era: str
    category: str
    modern_word: str | None
    modern_meaning: str
    classical_meaning: str | None
    example_sentence: str | None
    source: str | None


class DictionaryListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[DictionaryItem]


class DailyWordResponse(BaseModel):
    id: UUID
    word: str
    modern_meaning: str
    classical_meaning: str | None
    example_sentence: str | None
    source: str | None
    display_date: date | None