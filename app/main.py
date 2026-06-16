from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from sqlalchemy import text
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
from app.api.convert import router as convert_router
from app.api.dictionary import router as dictionary_router
from app.db import engine, AsyncSessionLocal
from app.models import Base

app = FastAPI(title="사라진 단어 복원기")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(convert_router, prefix="/api")
app.include_router(dictionary_router, prefix="/api")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health")
async def health():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    return {"status": "ok", "db": db_status, "version": "1.0.0"}
