import os
from dotenv import load_dotenv

load_dotenv()  
from app.config import settings

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import DefaultBotProperties
from aiogram.enums import ParseMode
from app.telegram_bot.handlers import router

bot = Bot(
    token=settings.TG_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()

dp.include_router(router)

dp.start_polling(bot) 
