import json
import os
from tqdm import tqdm
from reposurfer.core.embeddings.embedding_generator import EmbeddingGenerator
from reposurfer.core.embeddings.vector_store import VectorStore

def run_embedding(repo_path: str):
    print(f"[Phase2.3] Starting embedding generation...")
    
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

    print(f"[Phase2.3] Processing {len(chunks)} symbol chunks...")
    
    # Progress bar for embedding generation
    embedder = EmbeddingGenerator()
    
    # Show progress for embedding generation
    with tqdm(texts, desc="Generating embeddings", unit="chunk") as pbar:
        vectors = []
        for text in pbar:
            vector = embedder.embed([text])[0]
            vectors.append(vector)
            pbar.set_postfix({"dim": len(vector)})

    print(f"[Phase2.3] Storing vectors in database...")
    store = VectorStore(collection_name=repo_name)
    store.create(vector_size=len(vectors[0]))
    
    # Progress bar for storing
    with tqdm(range(0, len(ids), 100), desc="Storing in database", unit="batch") as pbar:
        for i in pbar:
            batch_end = min(i + 100, len(ids))
            batch_ids = ids[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_payloads = payloads[i:batch_end]
            
            store.upsert(batch_ids, batch_vectors, batch_payloads)
            pbar.set_postfix({"stored": batch_end, "total": len(ids)})

    print(f"[Phase2.3] Embedded and stored {len(vectors)} symbols")

if __name__ == "__main__":
    run_embedding("storage/repos/psf__requests")
