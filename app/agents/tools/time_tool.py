from langchain.tools import tool
from datetime import datetime

@tool
def get_time(query: str = "") -> str:
    """Вернёт текущее время в ISO формате. query - не используется."""
    return datetime.now().isoformat()