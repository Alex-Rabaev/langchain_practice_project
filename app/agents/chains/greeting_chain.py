from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.agents.memory.session_memory import get_history

SYSTEM = open("app/agents/prompts/system.md", encoding="utf-8").read()
GREETING = open("app/agents/prompts/greeting.md", encoding="utf-8").read()

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    ("placeholder", "{history}"),
    ("user", GREETING)
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
base_chain = prompt | llm | StrOutputParser()

# История будет подмешиваться автоматически
chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="name",     # ключ из inputs invoke({...})
    history_messages_key="history" # куда вставлять историю
)

def run_greeting(name: str, lang_code: str, session_id: str) -> str:
    # Плейсхолдеры из промптов: {name}, {lang_code}
    return chain.invoke(
        {"name": name, "lang_code": lang_code},
        config={"configurable": {"session_id": session_id}},
    )