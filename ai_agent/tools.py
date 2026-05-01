import os
import sys
from serpapi import GoogleSearch

from utils.logger import logger
from utils.exception import NetworkSecurityException
from dotenv import load_dotenv
load_dotenv()

def search_tool(query: str) -> str:
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": os.getenv("SERP_API_KEY"),
            "num": 5
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        snippets = []

        for res in results.get("organic_results", []):
            snippet = res.get("snippet")
            if snippet:
                snippets.append(snippet)

        if not snippets:
            return "No relevant external information found."

        return "\n\n".join(snippets)

    except Exception as e:
        logger.error("SERP API failed", exc_info=True)
        raise NetworkSecurityException(e, sys)
    
if __name__ == "__main__":
    query = "What is the latest news on cyber security?"
    print(search_tool(query))
    print(os.getenv("SERPAPI_API_KEY"))