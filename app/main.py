from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.api.endpoints import router as api_router
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    return {"status": "success", "message": "Database connection is working!"}