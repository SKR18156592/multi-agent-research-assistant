from graphs.research_graph import build_research_graph

graph = build_research_graph()
output = graph.invoke({"topic": "Quantum Computing in Finance", "max_analysts": 3})
print(output["final_report"])