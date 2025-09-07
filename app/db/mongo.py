from datetime import datetime, timezone
from pymongo import MongoClient, ASCENDING
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client.get_database(settings.MONGO_DB)

messages = db["messages"]
messages.create_index([("chat_id", ASCENDING), ("created_at", ASCENDING)])

def save_message(doc: dict) -> str:
    """
    Сохраняет сообщение (user/assistant) в коллекцию messages.
    doc: {
      "chat_id": str,
      "role": "user"|"assistant",
      "text": str,
      "meta": dict
    }
    """
    doc = dict(doc)
    doc.setdefault("created_at", datetime.now(timezone.utc))
    res = messages.insert_one(doc)
    return str(res.inserted_id)
