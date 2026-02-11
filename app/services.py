from openai import AsyncOpenAI
from app.core.config import settings
import logging

# Використовуємо асинхронний клієнт для FastAPI
client = AsyncOpenAI(
    base_url=settings.AI_BASE_URL, 
    api_key=settings.AI_API_KEY
)

async def get_ai_response(message_text: str, history: list):
    """
    history: список об'єктів повідомлень з БД
    """
    # Формуємо історію для контексту
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": message_text})
    
    try:
        response = await client.chat.completions.create(
            model=settings.AI_MODEL_NAME,
            messages=messages
        )
        
        usage = response.usage
        content = response.choices[0].message.content
        
        # Оскільки Groq безкоштовний, для ТЗ рахуємо за тарифами GPT-4o-mini:
        # $0.15 за 1M вхідних, $0.60 за 1M вихідних токенів
        cost = (usage.prompt_tokens * (0.15 / 1_000_000)) + \
               (usage.completion_tokens * (0.60 / 1_000_000))
        
        return {
            "content": content,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "cost": round(cost, 6)
        }
    except Exception as e:
        logging.error(f"AI API Error: {e}")
        raise e