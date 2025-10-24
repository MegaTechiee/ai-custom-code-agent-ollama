# 🧠 Custom Code Agent (Ollama + FAISS)

A lightweight, local-first coding assistant that reads your codebase and retrieves relevant answers - similar to GitHub Copilot, but focused on **context-aware understanding** of your own project.

---

## 🚀 Features

- 📁 **Codebase parsing and indexing** — Automatically scans and structures your project files.  
- 🧩 **Embeddings with `all-MiniLM-L6-v2`** — Converts code and docstrings into dense vector representations.  
- 🗂️ **FAISS vector database** — Efficiently stores and retrieves embeddings for semantic search.  
- 🦙 **LLM integration with `llama3`** — Generates context-aware answers from retrieved code snippets.  
- 💬 **Query interface (CLI)** — Ask natural language questions about your codebase.  
- ⚡ **Lightweight & local** — No external API calls required; privacy-friendly setup.

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Ollama** — for running local LLMs (e.g., llama3)
- **FAISS** — vector search for embedding retrieval
- **SentenceTransformers** — for `all-MiniLM-L6-v2` embeddings
- **Typer** — for building the CLI interface

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/ai-custom-code-agent-ollama.git
cd custom-code-agent-ollama

# Replace your codebase here ./embed_repo.py
repo_path = adjust your repo name

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .venv\Scripts\activate.ps1

# Install dependencies
pip install -r requirements.txt


