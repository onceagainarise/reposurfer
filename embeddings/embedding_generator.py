from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

    def embed(self, texts):
        return self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )
