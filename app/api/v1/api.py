from fastapi import APIRouter
from app.api.v1.endpoints import chat

# Створюємо головний роутер для v1
api_router = APIRouter()

# Підключаємо роутер чату
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])