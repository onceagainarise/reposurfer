import json
from phase2.retriever import RepoRetriever
from phase2.vector_store import VectorStore
from phase2.embedding_generator import EmbeddingGenerator

def run_retrieval(repo_path: str, query: str):
    with open(f"{repo_path}/symbol_graph.json") as f:
        symbol_graph = json.load(f)

    repo_name = repo_path.split("/")[-1]

    embedder = EmbeddingGenerator()
    store = VectorStore(collection_name=repo_name)
    store.create(vector_size=embedder.dim)
    retriever = RepoRetriever(
        vector_store=store,
        symbol_graph=symbol_graph,
        embedder=embedder
    )

    results = retriever.query(query, top_k=5)
    print(
    "Vector count:",
    store.client.count(store.collection, exact=True).count
)



    for r in results:
        print(f"[hybrid] {r['id']} ({r['type']}) score={r['score']:.3f}")
        print("File:", r.get("file",""))
        print(r.get("text","")[:200])


if __name__ == "__main__":
    run_retrieval(
        "storage/repos/psf__requests",
        "JSON decode error while parsing response"
    )
