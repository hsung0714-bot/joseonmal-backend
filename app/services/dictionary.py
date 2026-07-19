from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import ClassicalWord


async def get_classical_words(keywords: list[str], db: AsyncSession) -> dict[str, str]:
    """추출된 키워드를 DB에서 조회해서 현대어-고전어 치환 목록 반환"""
    substitutions = {}

    for keyword in keywords:
        result = await db.execute(
            select(ClassicalWord)
            .where(ClassicalWord.modern_word == keyword)
            .where(ClassicalWord.is_active == True)
            .limit(1)
        )
        word = result.scalar_one_or_none()
        if word:
            substitutions[keyword] = word.word

    return substitutions
