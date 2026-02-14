from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db, engine
from app.api.v1.api import api_router
from app.models import chat

chat.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.get("/new_session")
async def shortcut_new_session():
    # Цей ендпоінт просто перекидає користувача на правильний довгий шлях
    return RedirectResponse(url="/api/v1/chat/new_session")

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    return {"status": "success", "message": "Database connection is working!"}