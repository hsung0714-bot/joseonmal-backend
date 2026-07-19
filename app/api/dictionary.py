from uuid import UUID
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import ClassicalWord, DailyWord
from app.schemas.dictionary import (
    DictionaryItem,
    DictionaryListResponse,
    DailyWordResponse,
)

router = APIRouter()


@router.get("/dictionary", response_model=DictionaryListResponse)
async def get_dictionary(
    q: str | None = Query(default=None),
    category: str | None = Query(default=None),
    era: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(ClassicalWord).where(ClassicalWord.is_active == True)
    count_stmt = select(func.count()).select_from(ClassicalWord).where(ClassicalWord.is_active == True)

    if q:
        condition = or_(
            ClassicalWord.word.ilike(f"%{q}%"),
            ClassicalWord.modern_word.ilike(f"%{q}%"),
            ClassicalWord.modern_meaning.ilike(f"%{q}%"),
        )
        stmt = stmt.where(condition)
        count_stmt = count_stmt.where(condition)

    if category:
        stmt = stmt.where(ClassicalWord.category == category)
        count_stmt = count_stmt.where(ClassicalWord.category == category)

    if era:
        stmt = stmt.where(ClassicalWord.era == era)
        count_stmt = count_stmt.where(ClassicalWord.era == era)

    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    stmt = stmt.offset((page - 1) * size).limit(size)
    result = await db.execute(stmt)
    words = result.scalars().all()

    return DictionaryListResponse(
        total=total,
        page=page,
        size=size,
        items=[DictionaryItem.model_validate(word, from_attributes=True) for word in words],
    )


@router.get("/dictionary/daily", response_model=DailyWordResponse)
async def get_daily_word(db: AsyncSession = Depends(get_db)):
    today = date.today()

    result = await db.execute(
        select(ClassicalWord, DailyWord.display_date)
        .join(DailyWord, DailyWord.word_id == ClassicalWord.id)
        .where(DailyWord.display_date == today)
        .where(ClassicalWord.is_active == True)
        .limit(1)
    )

    row = result.first()

    if row is None:
        result = await db.execute(
            select(ClassicalWord)
            .where(ClassicalWord.is_active == True)
            .limit(1)
        )
        word = result.scalar_one_or_none()

        if word is None:
            raise HTTPException(status_code=404, detail="오늘의 단어가 없습니다.")

        return DailyWordResponse(
            id=word.id,
            word=word.word,
            modern_meaning=word.modern_meaning,
            classical_meaning=word.classical_meaning,
            example_sentence=word.example_sentence,
            source=word.source,
            display_date=None,
        )

    word, display_date = row

    return DailyWordResponse(
        id=word.id,
        word=word.word,
        modern_meaning=word.modern_meaning,
        classical_meaning=word.classical_meaning,
        example_sentence=word.example_sentence,
        source=word.source,
        display_date=display_date,
    )


@router.get("/dictionary/{word_id}", response_model=DictionaryItem)
async def get_dictionary_detail(
    word_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ClassicalWord)
        .where(ClassicalWord.id == word_id)
        .where(ClassicalWord.is_active == True)
    )

    word = result.scalar_one_or_none()

    if word is None:
        raise HTTPException(status_code=404, detail="단어를 찾을 수 없습니다.")

    return DictionaryItem.model_validate(word, from_attributes=True)