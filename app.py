from ai_agent.graph import build_graph

graph = build_graph()

while True:
    query = input("Ask: ")

    result = graph.invoke({
        "query": query
    })

    print("\nAnswer:\n", result["final_answer"])