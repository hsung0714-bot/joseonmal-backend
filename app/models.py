import uuid
from datetime import datetime, UTC
from sqlalchemy import String, Text, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ClassicalWord(Base):
    __tablename__ = "classical_words"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    word: Mapped[str] = mapped_column(String, index=True)
    era: Mapped[str] = mapped_column(Enum("조선전기", "조선후기", "고려", "삼국", name="era_enum"), index=True)
    category: Mapped[str] = mapped_column(Enum("감정어", "관계어", "일상어", "자연어", name="category_enum"))
    modern_meaning: Mapped[str] = mapped_column(Text)
    classical_meaning: Mapped[str] = mapped_column(Text)
    example_sentence: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
