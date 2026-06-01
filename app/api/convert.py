from fastapi import APIRouter, HTTPException
from app.schemas.convert import ConvertRequest, ConvertResponse, HighlightedWord
from app.services.morpheme import extract_keywords
from app.services.dictionary import get_classical_words
from app.services.claude_client import convert_to_classical

router = APIRouter()


@router.post("/convert", response_model=ConvertResponse)
async def convert(request: ConvertRequest):
    try:
        keywords = extract_keywords(request.original_text)
        substitutions = await get_classical_words(keywords)
        result = await convert_to_classical(request.original_text, substitutions)

        return ConvertResponse(
            converted_text=result["converted_text"],
            highlighted_words=[HighlightedWord(**w) for w in result["highlighted_words"]],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
