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
    
    # Generate all embeddings at once (more efficient)
    print(f"[Phase2.3] Generating embeddings for {len(texts)} chunks...")
    vectors = embedder.embed(texts)
    
    print(f"[Phase2.3] Storing vectors in database...")
    store = VectorStore(collection_name=repo_name)
    store.create(vector_size=len(vectors[0]))
    
    # Store in batches of 100
    batch_size = 100
    total_batches = (len(ids) + batch_size - 1) // batch_size
    
    with tqdm(range(total_batches), desc="Storing in database", unit="batch") as pbar:
        for i in pbar:
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, len(ids))
            
            batch_ids = ids[start_idx:end_idx]
            batch_vectors = vectors[start_idx:end_idx]
            batch_payloads = payloads[start_idx:end_idx]
            
            store.upsert(batch_ids, batch_vectors, batch_payloads)
            pbar.set_postfix({"stored": end_idx, "total": len(ids)})

    print(f"[Phase2.3] ✅ Embedded and stored {len(vectors)} symbols")

if __name__ == "__main__":
    run_embedding("storage/repos/psf__requests")
