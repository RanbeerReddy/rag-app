from ai_agent.rag import call_ollama

def rule_based_route(query: str) -> str:
    q = query.lower()

    debales_keywords = ["debales", "debales ai", "platform", "product"]
    comparison_keywords = ["vs", "compare", "competitor"]

    is_debales = any(k in q for k in debales_keywords)
    is_compare = any(k in q for k in comparison_keywords)

    if is_debales and is_compare:
        return "both"
    if is_debales:
        return "rag"

    return "unknown"


def llm_route(query: str) -> str:
    prompt = f"""You are the routing engine for the Debales AI assistant. 
Your job is to analyze the user's query and categorize it into exactly one of these three routes:

1. "rag": The user is asking specifically about Debales AI, its platform, features, or company details.
2. "both": The user is asking to compare Debales AI with a competitor, or requires a mix of Debales knowledge and general web knowledge.
3. "serp": The user is asking a general question, looking for recent news, or asking about something completely unrelated to Debales AI.

Respond strictly with ONLY one word: "rag", "both", or "serp". Do not add any punctuation or explanation.

User Query: "{query}"
Answer:"""
    
    response = call_ollama(prompt).strip().lower()

    if "both" in response:
        return "both"
    if "rag" in response:
        return "rag"
    return "serp"


def route_query(query: str) -> str:
    # Step 1: rule-based
    route = rule_based_route(query)

    if route != "unknown":
        return route

    # Step 2: fallback to LLM
    return llm_route(query)