import os
import json
import sys
import requests

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from utils.logger import logger
from utils.exception import NetworkSecurityException


# ---------------- LOAD DOCUMENTS ---------------- #
def load_documents(path="data/raw_docs.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            docs = json.load(f)

        texts = [doc["content"] for doc in docs]
        return texts

    except Exception as e:
        logger.error("Error loading documents", exc_info=True)
        raise NetworkSecurityException(e, sys)


# ---------------- EMBEDDINGS ---------------- #
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )


# ---------------- CREATE VECTORSTORE ---------------- #
def create_vectorstore(texts):
    try:
        embeddings = get_embeddings()

        vectorstore = FAISS.from_texts(texts, embedding=embeddings)
        vectorstore.save_local("vectorstore")

        logger.info("Vectorstore created and saved")

        return vectorstore

    except Exception as e:
        logger.error("Error creating vectorstore", exc_info=True)
        raise NetworkSecurityException(e, sys)


# ---------------- LOAD VECTORSTORE ---------------- #
def load_vectorstore():
    try:
        embeddings = get_embeddings()

        vectorstore = FAISS.load_local(
            "vectorstore",
            embeddings,
            allow_dangerous_deserialization=True
        )

        return vectorstore

    except Exception as e:
        logger.error("Error loading vectorstore", exc_info=True)
        raise NetworkSecurityException(e, sys)


# ---------------- RETRIEVAL ---------------- #
def retrieve_docs(query, k=3):
    try:
        vectorstore = load_vectorstore()
        #docs = vectorstore.similarity_search(query, k=k)
        docs = vectorstore.max_marginal_relevance_search(query, k=3, fetch_k=8)

        filtered = []
        for d in docs:
            if "debales" in d.page_content.lower():
                filtered.append(d.page_content)

        return filtered

        #return [doc.page_content for doc in docs]

    except Exception as e:
        logger.error("Error retrieving docs", exc_info=True)
        raise NetworkSecurityException(e, sys)


# ---------------- OLLAMA CALL ---------------- #
def call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]

    except Exception as e:
        logger.error("Error calling Ollama", exc_info=True)
        raise NetworkSecurityException(e, sys)


# ---------------- ANSWER GENERATION ---------------- #
def generate_answer(query, context):
    try:
        prompt = f"""
You are an AI assistant answering questions about Debales AI.

STRICT RULES:
- Answer ONLY from context
- Ignore irrelevant or unrelated information
- If context is mixed, extract only relevant parts
- If unsure, say: "I don’t have enough information"

Context:
{chr(10).join(context)}

Question:
{query}

Answer clearly and concisely:
"""

        return call_ollama(prompt)

    except Exception as e:
        logger.error("Error generating answer", exc_info=True)
        raise NetworkSecurityException(e, sys)


# ---------------- FULL PIPELINE ---------------- #
def rag_pipeline(query):
    try:
        docs = retrieve_docs(query)

        if not docs:
            return "I don’t have enough information to answer that."

        answer = generate_answer(query, docs)

        return answer

    except Exception as e:
        logger.error("RAG pipeline failed", exc_info=True)
        raise NetworkSecurityException(e, sys)


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    texts = load_documents()
    create_vectorstore(texts)

    while True:
        q = input("Ask: ")
        print(rag_pipeline(q))