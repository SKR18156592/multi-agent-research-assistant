# agents/interviewer.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from prompts.interview_prompts import INTERVIEWER_PROMPT

def interview_turn(analyst: dict, messages: list, model_name: str = "gpt-4o"):
    llm = ChatOpenAI(model=model_name, temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        ("system", INTERVIEWER_PROMPT.format(**analyst)),
        MessagesPlaceholder(variable_name="messages")
    ])
    chain = prompt | llm
    return chain.invoke({"messages": messages})