import sys
from src.graph import research_assistant_graph

def run_pipeline():
    topic = input("Enter research topic: ").strip()
    if not topic:
        topic = "The benefits of adopting LangGraph as an agent framework"

    max_analysts = 3
    thread = {"configurable": {"thread_id": "cli_session_1"}}

    print(f"\n[+] Initializing analyst generation for: '{topic}'...\n")
    initial_input = {"topic": topic, "max_analysts": max_analysts}

    # 1. Run until analyst review checkpoint
    for event in research_assistant_graph.stream(initial_input, thread, stream_mode="values"):
        analysts = event.get("analysts", [])
        if analysts:
            print(f"Generated {len(analysts)} Analyst Personas:")
            for a in analysts:
                print(f"- {a.name} ({a.role} | {a.affiliation})")
                print(f"  Focus: {a.description}\n")

    # 2. Human-In-The-Loop Loop
    while True:
        feedback = input("Provide feedback on personas (Press Enter to approve & continue): ").strip()
        if not feedback:
            research_assistant_graph.update_state(
                thread, 
                {"human_analyst_feedback": None}, 
                as_node="human_feedback"
            )
            break
        else:
            research_assistant_graph.update_state(
                thread, 
                {"human_analyst_feedback": feedback}, 
                as_node="human_feedback"
            )
            print("\n[+] Regenerating analysts based on feedback...\n")
            for event in research_assistant_graph.stream(None, thread, stream_mode="values"):
                analysts = event.get("analysts", [])
                if analysts:
                    for a in analysts:
                        print(f"- {a.name} ({a.role} | {a.affiliation})")
                        print(f"  Focus: {a.description}\n")

    # 3. Resume and complete full Map-Reduce parallel run
    print("\n[+] Running parallel interviews and synthesis pipeline...")
    for event in research_assistant_graph.stream(None, thread, stream_mode="updates"):
        node_name = next(iter(event.keys()))
        print(f"  -> Completed step: {node_name}")

    final_state = research_assistant_graph.get_state(thread)
    report = final_state.values.get("final_report", "")

    output_path = "final_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[✓] Research report completed and saved to `{output_path}`\n")

if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)