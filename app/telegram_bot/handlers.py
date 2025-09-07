import asyncio
from aiogram import Router, types
from aiogram.filters import CommandStart

from app.agents.chains.greeting_chain import run_greeting
from app.agents.support_agent import run_support
from app.db.mongo import save_message

router = Router()

def detect_lang(text: str) -> str:
    # Заглушка. Можешь подставить свою авто-детекцию.
    return "en"

@router.message(CommandStart())
async def on_start(message: types.Message):
    session_id = str(message.from_user.id)
    name = message.from_user.first_name or "Гость"
    lang = "en"  # или detect_lang(""), если хочешь

    # Логируем входящее
    await asyncio.to_thread(save_message, {
        "chat_id": session_id,
        "role": "user",
        "text": "/start",
        "meta": {"first_name": message.from_user.first_name, "username": message.from_user.username},
    })

    reply = run_greeting(name=name, lang_code=lang, session_id=session_id)

    # Логируем ответ ассистента
    await asyncio.to_thread(save_message, {
        "chat_id": session_id,
        "role": "assistant",
        "text": reply,
        "meta": {"type": "greeting"},
    })

    await message.answer(reply)

@router.message()
async def on_message(message: types.Message):
    session_id = str(message.from_user.id)
    text = message.text or ""
    lang = detect_lang(text)

    # Логируем входящее
    await asyncio.to_thread(save_message, {
        "chat_id": session_id,
        "role": "user",
        "text": text,
        "meta": {},
    })

    reply = run_support(text, lang_code=lang)

    # Логируем ответ ассистента
    await asyncio.to_thread(save_message, {
        "chat_id": session_id,
        "role": "assistant",
        "text": reply,
        "meta": {"type": "support"},
    })

    await message.answer(reply)