from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage
from graphs.state import InterviewState
from agents.interviewer import interview_turn
from utils.search import get_search_tool
from langchain_openai import ChatOpenAI
from prompts.report_prompts import SUMMARIZE_INTERVIEW_PROMPT

search_tool = get_search_tool()
llm = ChatOpenAI(model="gpt-4o", temperature=0)

def ask_question(state: InterviewState):
    response = interview_turn(state["analyst"], state["messages"])
    return {"messages": [response]}

def researcher_response(state: InterviewState):
    last_question = state["messages"][-1].content
    search_docs = search_tool.invoke(last_question)
    reply = llm.invoke(f"Answer this query: '{last_question}' using these search results: {search_docs}")
    return {"messages": [HumanMessage(content=reply.content)]}

def should_continue(state: InterviewState):
    # Max turns condition (e.g., 3 turns = 6 messages)
    if len(state["messages"]) >= 6:
        return "summarize"
    return "researcher"

def summarize(state: InterviewState):
    chat_history = "\n".join([f"{m.type}: {m.content}" for m in state["messages"]])
    prompt = SUMMARIZE_INTERVIEW_PROMPT.format(
        name=state["analyst"]["name"], 
        messages=chat_history
    )
    summary = llm.invoke(prompt).content
    return {"interview_summary": summary}

def build_interview_graph():
    builder = StateGraph(InterviewState)
    builder.add_node("interviewer", ask_question)
    builder.add_node("researcher", researcher_response)
    builder.add_node("summarize", summarize)

    builder.add_edge(START, "interviewer")
    builder.add_conditional_edges("interviewer", should_continue, {
        "researcher": "researcher",
        "summarize": "summarize"
    })
    builder.add_edge("researcher", "interviewer")
    builder.add_edge("summarize", END)
    
    return builder.compile()