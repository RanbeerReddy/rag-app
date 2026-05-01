def route_query(query: str) -> str:
    q = query.lower()

    debales_keywords = [
        "debales",
        "debales ai",
        "their platform",
        "their product",
        "their service",
        "company",
        "this company",
        "their system"
    ]

    comparison_keywords = [
        "vs",
        "compare",
        "difference",
        "competitor",
        "better than"
    ]

    general_keywords = [
        "news",
        "latest",
        "trend",
        "what is",
        "who is",
        "define",
        "history"
    ]

    # scoring system (more robust than binary)
    score = {
        "rag": 0,
        "serp": 0
    }

    # Debales detection
    for k in debales_keywords:
        if k in q:
            score["rag"] += 2

    # comparison → mixed
    for k in comparison_keywords:
        if k in q:
            score["rag"] += 1
            score["serp"] += 1

    # general queries
    for k in general_keywords:
        if k in q:
            score["serp"] += 2

    # final decision
    if score["rag"] > 0 and score["serp"] > 0:
        return "both"

    if score["rag"] > score["serp"]:
        return "rag"

    return "serp"