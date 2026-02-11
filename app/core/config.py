from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    AI_API_KEY: str
    AI_MODEL_NAME: str
    AI_BASE_URL : str
    DATABASE_URL: str = "sqlite:///./chat_history.db"
    
    # Ціни для розрахунку
    PRICE_INPUT_1M: float = 0.25
    PRICE_OUTPUT_1M: float = 2.00

    # Налаштування завантаження
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()