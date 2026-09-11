from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from extra.graphs.state import ResearchState, InterviewState
from agents.analyst import create_analysts
from graphs.interview_graph import build_interview_graph
from prompts.report_prompts import FINAL_REPORT_COMPILER_PROMPT
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
interview_subgraph = build_interview_graph()

def generate_analysts_node(state: ResearchState):
    analysts = create_analysts(state["topic"], state["max_analysts"])
    return {"analysts": analysts}

def initiate_interviews(state: ResearchState):
    return [
        Send("interview_node", {
            "analyst": analyst,
            "messages": [],
            "interview_summary": None
        })
        for analyst in state["analysts"]
    ]

def run_subgraph_interview(state: InterviewState):
    result = interview_subgraph.invoke(state)
    return {"sections": [result["interview_summary"]]}

def compile_final_report(state: ResearchState):
    sections_text = "\n\n---\n\n".join(state["sections"])
    prompt = FINAL_REPORT_COMPILER_PROMPT.format(
        topic=state["topic"],
        sections=sections_text
    )
    report = llm.invoke(prompt).content
    return {"final_report": report}

def build_research_graph():
    builder = StateGraph(ResearchState)
    builder.add_node("generate_analysts", generate_analysts_node)
    builder.add_node("interview_node", run_subgraph_interview)
    builder.add_node("compile_report", compile_final_report)

    builder.add_edge(START, "generate_analysts")
    builder.add_conditional_edges("generate_analysts", initiate_interviews, ["interview_node"])
    builder.add_edge("interview_node", "compile_report")
    builder.add_edge("compile_report", END)

    return builder.compile()

def build_research_graph():
    # Add nodes and edges 
    builder=StateGraph(ResearchGraphState)
    builder.add_node(create_analysts)
    builder.add_node(human_feedback)
    builder.add_node('conduct_interview',interview_builder.compile())
    builder.add_node(write_conclusion)
    builder.add_node(write_introduction)
    builder.add_node(write_report)
    builder.add_node(finalize_report)

    # Logic
    builder.add_edge(START,'create_analysts')
    builder.add_edge('create_analysts','human_feedback')
    builder.add_conditional_edges('human_feedback',intialize_all_interview,['create_analysts','conduct_interview'])
    builder.add_edge('conduct_interview','write_conclusion')
    builder.add_edge('conduct_interview','write_introduction')
    builder.add_edge('conduct_interview','write_report')
    builder.add_edge('write_conclusion','finalize_report')
    builder.add_edge('write_introduction','finalize_report')
    builder.add_edge('write_report','finalize_report')

    # Compile
    memory=MemorySaver()
    graph=builder.compile(interrupt_before=['human_feedback'],checkpointer=memory)
    display(Image(graph.get_graph(xray=1).draw_mermaid_png()))