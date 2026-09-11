from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, get_buffer_string
from langgraph.graph import START, END, StateGraph
from src.config import get_llm
from src.models import InterviewState, SearchQuery
from src.tools import fetch_web_search, fetch_wikipedia_search
from src.prompts import (
    QUESTION_INSTRUCTIONS, 
    SEARCH_INSTRUCTIONS, 
    ANSWER_INSTRUCTIONS, 
    SECTION_WRITER_INSTRUCTIONS
)

llm = get_llm()

def generate_question(state: InterviewState):
    analyst = state["analyst"]
    messages = state["messages"]
    system_message = QUESTION_INSTRUCTIONS.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)
    return {"messages": [question]}

def search_web(state: InterviewState):
    structured_llm = llm.with_structured_output(SearchQuery)
    query_result = structured_llm.invoke([SystemMessage(content=SEARCH_INSTRUCTIONS)] + state["messages"])
    formatted_docs = fetch_web_search(query_result.search_query)
    return {"context": [formatted_docs]}

def search_wikipedia(state: InterviewState):
    structured_llm = llm.with_structured_output(SearchQuery)
    query_result = structured_llm.invoke([SystemMessage(content=SEARCH_INSTRUCTIONS)] + state["messages"])
    formatted_docs = fetch_wikipedia_search(query_result.search_query)
    return {"context": [formatted_docs]}

def generate_answer(state: InterviewState):
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]
    system_message = ANSWER_INSTRUCTIONS.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_message)] + messages)
    answer.name = "expert"
    return {"messages": [answer]}

def save_interview(state: InterviewState):
    interview_str = get_buffer_string(state["messages"])
    return {"interview": interview_str}

def route_messages(state: InterviewState, name: str = "expert"):
    messages = state["messages"]
    max_num_turns = state.get("max_num_turns", 2)
    num_responses = len([m for m in messages if isinstance(m, AIMessage) and getattr(m, "name", None) == name])

    if num_responses >= max_num_turns:
        return "save_interview"

    last_question = messages[-2]
    if "Thank you so much for your help!" in last_question.content:
        return "save_interview"
    return "ask_question"

def write_section(state: InterviewState):
    context = state["context"]
    analyst = state["analyst"]
    system_message = SECTION_WRITER_INSTRUCTIONS.format(focus=analyst.description)
    section = llm.invoke(
        [SystemMessage(content=system_message)] + 
        [HumanMessage(content=f"use this source to write your section: {context}")]
    )
    return {"sections": [section.content]}

interview_builder = StateGraph(InterviewState)
interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_wikipedia", search_wikipedia)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_wikipedia")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_wikipedia", "answer_question")
interview_builder.add_conditional_edges("answer_question", route_messages, ["ask_question", "save_interview"])
interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)

interview_subgraph = interview_builder.compile()