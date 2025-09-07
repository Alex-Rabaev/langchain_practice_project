import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST", "")
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET", "")

    TG_BOT_TOKEN: str = os.getenv("TG_BOT_TOKEN", "")

    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB: str = os.getenv("MONGO_DB", "")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

settings = Settings()