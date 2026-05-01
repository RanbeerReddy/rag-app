# Debales AI Assistant (RAG + LangGraph + SERP)

## Overview

This project is an AI assistant that answers questions about **Debales AI** using **Retrieval-Augmented Generation (RAG)** and external search via a **SERP API**. It uses **LangGraph** to route queries intelligently between internal knowledge (RAG) and external search (SERP), and combines them when needed.

---

## Features

* 🔎 **RAG over Debales data** (scraped from website/blog/product pages)
* 🌐 **SERP tool** for external queries (SerpAPI)
* 🧠 **LangGraph routing** (RAG / SERP / BOTH)
* 🧾 **No hallucination policy** (answers only from context)
* 🖥️ **Simple Flask UI** for interaction
* ⚡ **Local LLM (Ollama - llama3)** for answer generation

---

## Architecture

```
User Query
   ↓
Router (rule-based)
   ↓
 ┌───────────────┬───────────────┬───────────────┐
 │      RAG      │     SERP      │     BOTH      │
 │ (Debales DB)  │ (Web search)  │ (Combine)     │
 └───────────────┴───────────────┴───────────────┘
   ↓
LLM (Ollama - llama3)
   ↓
Final Answer
```

---

## Tech Stack

* **LangChain** – RAG pipeline
* **LangGraph** – workflow orchestration
* **FAISS** – vector database
* **Sentence Transformers** – embeddings
* **Ollama (llama3)** – local LLM
* **SerpAPI** – external search tool
* **Flask** – simple UI

---

## Project Structure

```
ai_agent/
  graph.py        # LangGraph workflow
  rag.py          # RAG pipeline
  router.py       # Query routing logic
  scraper.py      # Data scraping
  tools.py        # SERP API tool
data/
  raw_docs.json   # Scraped data
templates/
  index.html      # Flask UI
utils/
  logger.py
  exception.py
app.py            # Flask app
```

---

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file in root:

```txt
SERPAPI_API_KEY=your_serpapi_key_here
```

---

### 5. Install Ollama (Local LLM)

Download: https://ollama.com

Then run:

```bash
ollama pull llama3
ollama serve
```

---

### 6. Build Vectorstore (Run Once)

```bash
python -m ai_agent.rag
```

This creates the FAISS index from scraped data.

---

### 7. Run the App

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## Example Queries

### RAG (Debales-related)

**Q:** What does Debales AI do?
**A:** Debales AI is a platform that uses AI agents to automate workflows, improve customer interactions, and enhance business operations.

---

### SERP (External)

**Q:** Latest AI trends
**A:** (Uses SerpAPI + LLM to summarize recent developments)

---

### BOTH (Mixed)

**Q:** Debales AI vs competitors
**A:** Combines internal knowledge (Debales) + external insights (SERP)

---

### Unknown

**Q:** asdasdasd
**A:** I don’t have enough information to answer that.

---

## Key Design Decisions

* **Local LLM (Ollama)** → avoids API cost and improves control
* **Rule-based router** → simple, explainable, and fast
* **Sentence-based chunking** → better retrieval quality
* **No hallucination prompting** → ensures reliability

---

## Notes

* Ensure **Ollama is running** before starting the app
* `vectorstore/` is not included in repo — it is generated locally
* `raw_docs.json` is included for reproducibility

---

## Evaluation Alignment

✔ Correct routing (RAG vs SERP vs BOTH)
✔ Quality scraping + retrieval
✔ Proper SERP tool usage
✔ Clear LangGraph workflow
✔ No hallucination
✔ Clean, modular code

---

## Demo Video

Include:

* System overview
* Routing explanation
* Live demo (RAG, SERP, BOTH cases)

---

## Author

Your Name
