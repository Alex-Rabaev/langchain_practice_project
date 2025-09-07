from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from app.agents.tools.time_tool import get_time
from app.agents.tools.db_tool import get_faq

REACT_SYSTEM = """Ты — поддержка Telegram-бота.
Отвечай кратко и по делу. Язык ответа: {lang_code}.

У тебя есть доступ к следующим инструментам:

{tools}

Используй следующий формат:

Question: вопрос пользователя
Thought: что ты думаешь о том, что нужно сделать
Action: действие, которое нужно выполнить, должно быть одним из [{tool_names}]
Action Input: входные данные для действия
Observation: результат действия
... (этот процесс Thought/Action/Action Input/Observation может повторяться N раз)
Thought: теперь я знаю окончательный ответ
Final Answer: окончательный ответ пользователю

Начни!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate(
    template=REACT_SYSTEM,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names", "lang_code"]
)

def build_support_agent(lang_code: str = "ru") -> AgentExecutor:
    tools = [get_time, get_faq]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    react_prompt = prompt.partial(lang_code=lang_code)  # подставим язык заранее

    agent = create_react_agent(llm, tools, react_prompt)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,   # немного терпимости к форматированию
    )

def run_support(question: str, lang_code: str = "ru") -> str:
    executor = build_support_agent(lang_code)
    result = executor.invoke({"input": question})
    return result["output"]