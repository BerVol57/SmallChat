from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1", 
    api_key=os.getenv("AI_API_KEY")
)

model_name = os.getenv("AI_MODEL_NAME")

try:
    response = client.chat.completions.create(
        model=model_name, 
        messages=[{"role": "user", "content": "Say 'Connection OK'"}],
        max_tokens=5
    )
    print(f"Відповідь від AI: {response.choices[0].message.content}")
except Exception as e:
    print(f"Сталася помилка при запиті: {e}")