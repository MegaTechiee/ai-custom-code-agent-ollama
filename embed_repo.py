
import os
import glob
from sentence_transformers import SentenceTransformer
import faiss
import pickle

# repo_path = "D:\\Projects\\AI\\emp-leave-management-server"


def load_code_files(repo_path, extensions=[".go", ".js", ".py", ".ts", ".java", ".c", ".cpp", ".h", ".hpp", ".php", ".sql"]):
    code_files = []
    for ext in extensions:
        for file in glob.glob(f"{repo_path}/**/*{ext}", recursive=True):
            if os.path.isfile(file):
                code_files.append(file)
    return code_files


def chunk_text(text, chunk_size=500):
    lines = text.splitlines()
    chunks, current = [], []
    count = 0
    for line in lines:
        current.append(line)
        count += len(line)
        if count >= chunk_size:
            chunks.append("\n".join(current))
            current, count = [], 0
    if current:
        chunks.append("\n".join(current))
    return chunks


def embed_and_store(chunks, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    vectors = model.encode(chunks)

    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    faiss.write_index(index, "index.faiss")
    print("Embeddings stored/updated.")


if __name__ == "__main__":
    repo_path = "../emp-leave-management-server"  # adjust your repo name
    files = load_code_files(repo_path)

    all_chunks = []
    for file in files:
        with open(file, "r", errors="ignore") as f:
            code = f.read()
            chunks = chunk_text(code)
            all_chunks.extend(chunks)

    embed_and_store(all_chunks)
