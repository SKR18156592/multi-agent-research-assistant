from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send
from langchain_core.messages import SystemMessage, HumanMessage

from src.config import get_llm
from src.models import ResearchGraphState, Perspectives
from src.prompts import (
    ANALYST_INSTRUCTIONS, 
    REPORT_WRITER_INSTRUCTIONS, 
    INTRO_CONCLUSION_INSTRUCTIONS
)
from src.subgraphs.interview import interview_subgraph

llm = get_llm()

def create_analysts(state: ResearchGraphState):
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback", "")

    structured_llm = llm.with_structured_output(Perspectives)
    system_message = ANALYST_INSTRUCTIONS.format(
        topic=topic,
        max_analysts=max_analysts,
        human_analyst_feedback=human_analyst_feedback
    )
    analysts = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Generate the set of analysts")
    ])
    return {"analysts": analysts.analysts}

def human_feedback(state: ResearchGraphState):
    """No-op node configured for interruptions."""
    pass

def initialize_all_interviews(state: ResearchGraphState):
    if state.get("human_analyst_feedback"):
        return "create_analysts"

    topic = state["topic"]
    return [
        Send(
            "conduct_interview", 
            {
                "analyst": analyst,
                "messages": [HumanMessage(content=f"So you said you were writing an article on {topic}?")]
            }
        )
        for analyst in state["analysts"]
    ]

def write_report(state: ResearchGraphState):
    sections = state["sections"]
    topic = state["topic"]
    formatted_sections = "\n\n".join(sections)
    system_message = REPORT_WRITER_INSTRUCTIONS.format(topic=topic, context=formatted_sections)
    report = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="Write a report based upon these memos")
    ])
    return {"content": report.content}

def write_introduction(state: ResearchGraphState):
    sections = state["sections"]
    topic = state["topic"]
    formatted_sections = "\n\n".join(sections)
    instructions = INTRO_CONCLUSION_INSTRUCTIONS.format(topic=topic, formatted_str_sections=formatted_sections)
    intro = llm.invoke([
        SystemMessage(content=instructions),
        HumanMessage(content="write the report introduction")
    ])
    return {"introduction": intro.content}

def write_conclusion(state: ResearchGraphState):
    sections = state["sections"]
    topic = state["topic"]
    formatted_sections = "\n\n".join(sections)
    instructions = INTRO_CONCLUSION_INSTRUCTIONS.format(topic=topic, formatted_str_sections=formatted_sections)
    conclusion = llm.invoke([
        SystemMessage(content=instructions),
        HumanMessage(content="write the report conclusion")
    ])
    return {"conclusion": conclusion.content}

def finalize_report(state: ResearchGraphState):
    content = state["content"].removeprefix("## Insights").lstrip()
    sources = None
    if "\n## Sources\n" in content:
        content, sources = content.split("\n## Sources\n", maxsplit=1)

    final_report = f"{state['introduction']}\n\n---\n\n{content}\n\n---\n\n{state['conclusion']}"
    if sources:
        final_report += f"\n\n## Sources\n{sources}"

    return {"final_report": final_report}

# Build Main Orchestrator Graph
builder = StateGraph(ResearchGraphState)
builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("conduct_interview", interview_subgraph)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("write_introduction", write_introduction)
builder.add_node("write_report", write_report)
builder.add_node("finalize_report", finalize_report)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges(
    "human_feedback",
    initialize_all_interviews,
    ["create_analysts", "conduct_interview"]
)
builder.add_edge("conduct_interview", "write_conclusion")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_report")
builder.add_edge("write_conclusion", "finalize_report")
builder.add_edge("write_introduction", "finalize_report")
builder.add_edge("write_report", "finalize_report")

checkpointer = MemorySaver()
research_assistant_graph = builder.compile(
    interrupt_before=["human_feedback"],
    checkpointer=checkpointer
)