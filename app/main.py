from fastapi import FastAPI
from app.api.convert import router as convert_router

app = FastAPI(title="사라진 단어 복원기")

app.include_router(convert_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
