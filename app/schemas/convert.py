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
