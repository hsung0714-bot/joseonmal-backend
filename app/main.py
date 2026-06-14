from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
from app.api.convert import router as convert_router

app = FastAPI(title="사라진 단어 복원기")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(convert_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
