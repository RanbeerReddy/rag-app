import requests
from bs4 import BeautifulSoup
import json
import os
import time
import sys

from utils.logger import logger
from utils.exception import NetworkSecurityException


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}



def fetch_page(url: str) -> str:
    try:
        logger.info(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    except Exception as e:
        logger.error(f"Failed to fetch {url}", exc_info=True)
        raise NetworkSecurityException(e, sys)



def clean_html(soup: BeautifulSoup):
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    return soup


def extract_text(html: str) -> str:
    try:
        soup = BeautifulSoup(html, "html.parser")
        soup = clean_html(soup)

        texts = []

        for tag in soup.find_all(["h1", "h2", "h3", "p"]):
            text = tag.get_text().strip()
            if text:
                texts.append(text)

        combined_text = " ".join(texts)
        combined_text = " ".join(combined_text.split())

        return combined_text

    except Exception as e:
        logger.error("Text extraction failed", exc_info=True)
        raise NetworkSecurityException(e, sys)



def remove_noise(text: str) -> str:
    noise_phrases = [
        "Still have a question",
        "Answered.",
        "Your Questions",
        "See running on your actual freight data"
    ]

    for phrase in noise_phrases:
        text = text.replace(phrase, "")

    return text



def clean_repetition(text: str) -> str:
    sentences = text.split(". ")
    seen = set()
    cleaned = []

    for s in sentences:
        if s not in seen:
            seen.add(s)
            cleaned.append(s)

    return ". ".join(cleaned)


def split_chunks(text: str, chunk_size=500):
    sentences = text.split(". ")

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks



def is_good_chunk(chunk):
    return len(chunk.split()) > 20



def scrape_urls(urls: list) -> list:
    documents = []

    for url in urls:
        try:
            html = fetch_page(url)
            if not html:
                continue

            text = extract_text(html)
            text = remove_noise(text)
            text = clean_repetition(text)

            chunks = split_chunks(text)

            for chunk in chunks:
                if is_good_chunk(chunk):
                    documents.append({
                        "content": chunk,
                        "source": url
                    })

            logger.info(f"Scraped & processed: {url}")
            time.sleep(1)

        except NetworkSecurityException:
            continue

    return documents



def remove_duplicates(docs):
    seen = set()
    unique_docs = []

    for doc in docs:
        content = doc["content"]

        if content not in seen:
            seen.add(content)
            unique_docs.append(doc)

    return unique_docs



def save_docs(docs, path="data/raw_docs.json"):
    try:
        os.makedirs("data", exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(docs)} documents")

    except Exception as e:
        logger.error("Saving failed", exc_info=True)
        raise NetworkSecurityException(e, sys)



if __name__ == "__main__":
    
    urls = [
            "https://debales.ai/",
            "https://debales.ai/book-demo",
            "https://debales.ai/ai-agent",
            "https://debales.ai/ai-agent/rerouting",
            "https://debales.ai/ai-agent/multi-agent",
            "https://debales.ai/ai-agent/load-planning",
            "https://debales.ai/ai-agent/fleet",
            "https://debales.ai/ai-agent/ai-crm",
            "https://debales.ai/ai-agent/orchestrator",
            "https://debales.ai/logistics",
            "https://debales.ai/integrations",
            "https://debales.ai/ecommerce",
            "https://debales.ai/case-studies",
            "https://debales.ai/case-studies/debales-ai-cuts-customer-support-requests-for-blossom-and-rhyme",
            
        ]

    docs = scrape_urls(urls)
    docs = remove_duplicates(docs)

    save_docs(docs)

    print(f"✅ Final documents count: {len(docs)}")


urls = [
        "https://debales.ai/",
        "https://debales.ai/book-demo",
        "https://debales.ai/ai-agent",
        "https://debales.ai/ai-agent/rerouting",
        "https://debales.ai/ai-agent/multi-agent",
        "https://debales.ai/ai-agent/load-planning",
        "https://debales.ai/ai-agent/fleet",
        "https://debales.ai/ai-agent/ai-crm",
        "https://debales.ai/ai-agent/orchestrator",
        "https://debales.ai/logistics",
        "https://debales.ai/integrations",
        "https://debales.ai/ecommerce",
        "https://debales.ai/case-studies",
        "https://debales.ai/case-studies/debales-ai-cuts-customer-support-requests-for-blossom-and-rhyme",
        
    ]
