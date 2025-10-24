import pickle
import subprocess
import sys
import faiss
from sentence_transformers import SentenceTransformer
import requests

EXIT_COMMANDS = {"bye", "exit", "quit", "q"}


def update_embeddings():
    subprocess.run([sys.executable, "embed_repo.py"], check=True)


def load_resources():
    update_embeddings()
    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    index = faiss.read_index("index.faiss")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return chunks, index, model


def search_similar_chunks(query, chunks, index, model, k=5):
    query_vec = model.encode([query])
    distances, indices = index.search(query_vec, k)
    results = [chunks[i] for i in indices[0]]
    return results


def ask_ollama(context_chunks, question):
    prompt = "Answer the following question based on the code context. For each code snippet you reference, include the actual code in your response:\n"
    for i, chunk in enumerate(context_chunks):
        prompt += f"\n--- SNIPPET {i+1} ---\n{chunk}\n"
    prompt += f"\n\nQuestion: {question}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=1000,
    )
    return response.json().get("response", "")


if __name__ == "__main__":
    chunks, index, model = load_resources()
    try:
        while True:
            question = input("Ask a question (type 'bye' to exit): ").strip()
            if not question:
                continue
            if question.lower() in EXIT_COMMANDS:
                print("Goodbye.")
                break
            context = search_similar_chunks(question, chunks, index, model)
            answer = ask_ollama(context, question)
            print("\nAnswer from Ollama:\n", answer, "\n")
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
