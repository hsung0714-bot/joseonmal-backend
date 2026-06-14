from fastapi import FastAPI
from sqlalchemy import text
from app.db.database import Base, engine, SessionLocal
from app.models import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="사라진 단어 복원기 API")

@app.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_status = "ok"
    except Exception:
        db_status = "error"
    
    return {
        "status": "ok",
        "db": db_status,
        "version": "1.0.0"
    }