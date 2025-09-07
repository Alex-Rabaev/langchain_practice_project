from langchain.tools import tool

_FAKE_DB = {
    "faq": "Мы работаем пн-пт с 9:00 до 18:00. Доставка по Израилю 1-3 дня."
}

@tool
def get_faq(query: str = "") -> str:
    """Вернёт FAQ из условной БД (пример). query - поисковый запрос (не используется в этом примере)."""
    return _FAKE_DB["faq"]