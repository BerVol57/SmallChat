from fastapi import APIRouter
from app.api.v1.endpoints import chat

# Створюємо головний роутер для v1
api_router = APIRouter()

# Підключаємо роутер чату
# Тепер усі запити до чату матимуть префікс /chat, наприклад: /api/v1/chat/sessions
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Якщо у майбутньому будуть інші модулі, додаємо їх так само:
# api_router.include_router(users.router, prefix="/users", tags=["users"])