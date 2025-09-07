from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram import types
from dotenv import load_dotenv

from app.config import settings
from app.telegram_bot.handlers import router as telegram_router
from app.db.mongo import save_message  # логировать будем прямо отсюда при желании

load_dotenv()

# Инициализация бота и диспетчера один раз на процесс
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=settings.TG_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
dp.include_router(telegram_router)

WEBHOOK_PATH = "/telegram/webhook"
WEBHOOK_URL = settings.WEBHOOK_HOST.rstrip("/") + WEBHOOK_PATH

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if not settings.WEBHOOK_HOST:
        raise RuntimeError("WEBHOOK_HOST is not set. Please set it in .env")
    await bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=settings.WEBHOOK_SECRET,
        drop_pending_updates=True,
    )
    yield
    # Shutdown
    await bot.delete_webhook(drop_pending_updates=False)

app = FastAPI(
    title="Telegram Bot via Webhook + LangChain + Mongo",
    lifespan=lifespan
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    # Проверяем секрет заголовка
    header = request.headers.get("x-telegram-bot-api-secret-token")
    if settings.WEBHOOK_SECRET and header != settings.WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    data = await request.json()
    update = types.Update.model_validate(data)

    # Прокидываем апдейт в aiogram
    await dp.feed_update(bot, update)
    return {"ok": True}