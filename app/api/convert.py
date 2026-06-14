from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.convert import ConvertRequest, ConvertResponse, HighlightedWord
from app.services.morpheme import extract_keywords
from app.services.dictionary import get_classical_words
from app.services.claude_client import convert_to_classical
from app.db import get_db
from app.limiter import limiter

router = APIRouter()


@router.post("/convert", response_model=ConvertResponse)
@limiter.limit("10/minute")
async def convert(request: Request, body: ConvertRequest, db: AsyncSession = Depends(get_db)):
    try:
        keywords = extract_keywords(body.original_text)
        substitutions = await get_classical_words(keywords, db)
        result = await convert_to_classical(body.original_text, substitutions)

        return ConvertResponse(
            converted_text=result["converted_text"],
            highlighted_words=[HighlightedWord(**w) for w in result["highlighted_words"]],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
