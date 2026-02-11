from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    return {"status": "success", "message": "Database connection is working!"}