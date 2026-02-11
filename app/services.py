from openai import AsyncOpenAI
from app.core.config import settings
import logging

# Використовуємо асинхронний клієнт для FastAPI
client = AsyncOpenAI(
    base_url=settings.AI_BASE_URL, 
    api_key=settings.AI_API_KEY
)

price_in_1m = settings.PRICE_INPUT_1M
price_out_1m = settings.PRICE_OUTPUT_1M

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
        
        cost = (usage.prompt_tokens * (price_in_1m / 1_000_000)) + \
               (usage.completion_tokens * (price_out_1m / 1_000_000))
        
        return {
            "content": content,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "cost": round(cost, 6)
        }
    except Exception as e:
        logging.error(f"AI API Error: {e}")
        raise e