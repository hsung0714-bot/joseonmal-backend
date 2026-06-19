import uuid
from sqlalchemy import Column, String, Text, Boolean, Date, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
from app.db.database import Base

class EraEnum(str, enum.Enum):
    joseon_early = "조선전기"
    joseon_late = "조선후기"
    goryeo = "고려"
    samguk = "삼국"

class CategoryEnum(str, enum.Enum):
    emotion = "감정어"
    relation = "관계어"
    daily = "일상어"
    nature = "자연어"

class ClassicalWord(Base):
    __tablename__ = "classical_words"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word = Column(String, nullable=False, index=True)
    era = Column(Enum("조선전기", "조선후기", "고려", "삼국", name="era_enum"), nullable=False, index=True)
    category = Column(Enum("감정어", "관계어", "일상어", "자연어", name="category_enum"), nullable=True)
    modern_word = Column(String, nullable=True)
    modern_meaning = Column(Text, nullable=False)
    classical_meaning = Column(Text, nullable=True)
    example_sentence = Column(Text, nullable=True)
    source = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DailyWord(Base):
    __tablename__ = "daily_words"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word_id = Column(UUID(as_uuid=True), ForeignKey("classical_words.id"), nullable=False)
    display_date = Column(Date, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
