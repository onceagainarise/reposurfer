import json
from phase2.embedding_generator import EmbeddingGenerator
from phase2.vector_store import VectorStore

def run_embedding(repo_path: str):
    with open(f"{repo_path}/symbol_chunks.json") as f:
        chunks = json.load(f)
    repo_name = repo_path.split("/")[-1]
    texts = [c["text"] for c in chunks]
    ids = list(range(len(texts)))
    payloads = [
        {
            "symbol_id": c["symbol_id"],
            "symbol_type": c["symbol_type"],
            "file": c["file"]
        }
        for c in chunks
    ]

    embedder = EmbeddingGenerator()
    vectors = embedder.embed(texts)

    store = VectorStore(collection_name=repo_name)
    store.create(vector_size=len(vectors[0]))
    store.upsert(ids, vectors, payloads)

    print(f"[Phase2.3] Embedded {len(vectors)} symbols")

if __name__ == "__main__":
    run_embedding("storage/repos/psf__requests")
