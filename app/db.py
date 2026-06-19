import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

_url = os.getenv("DATABASE_URL", "")
DATABASE_URL = _url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
