from langgraph.graph import StateGraph, END
from typing import TypedDict

from ai_agent.rag import rag_pipeline
from ai_agent.tools import search_tool
from ai_agent.router import route_query

class AgentState(TypedDict):
    query: str
    route: str
    rag_response: str
    serp_response: str
    final_answer: str

def router_node(state: AgentState):
    route = route_query(state["query"])
    return {"route": route}


def rag_node(state: AgentState):
    response = rag_pipeline(state["query"])
    return {"rag_response": response}

def serp_node(state: AgentState):
    response = search_tool(state["query"])

    # IMPORTANT: pass SERP result through LLM
    from ai_agent.rag import generate_answer
    final = generate_answer(state["query"], [response])

    return {"serp_response": final}

def both_node(state: AgentState):
    rag_resp = rag_pipeline(state["query"])

    serp_raw = search_tool(state["query"])

    from ai_agent.rag import generate_answer
    serp_resp = generate_answer(state["query"], [serp_raw])

    combined = f"""
RAG Answer:
{rag_resp}

External Info:
{serp_resp}
"""

    return {
        "rag_response": rag_resp,
        "serp_response": serp_resp,
        "final_answer": combined
    }

def final_node(state: AgentState):
    route = state["route"]

    if route == "rag":
        return {"final_answer": state["rag_response"]}

    elif route == "serp":
        return {"final_answer": state["serp_response"]}

    return {"final_answer": state.get("final_answer", "No answer available")}



def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("rag", rag_node)
    builder.add_node("serp", serp_node)
    builder.add_node("both", both_node)
    builder.add_node("final", final_node)

    builder.set_entry_point("router")

    # Routing logic
    def route_decision(state):
        return state["route"]

    builder.add_conditional_edges(
        "router",
        route_decision,
        {
            "rag": "rag",
            "serp": "serp",
            "both": "both"
        }
    )

    # Flow
    builder.add_edge("rag", "final")
    builder.add_edge("serp", "final")
    builder.add_edge("both", "final")

    builder.set_finish_point("final")

    return builder.compile()