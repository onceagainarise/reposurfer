from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from qdrant_client.http.models import CollectionStatus

class VectorStore:
    def __init__(self, collection_name: str, storage_path="storage/qdrant"):
        self.collection = collection_name
        self.client = QdrantClient(path=storage_path)

    def create(self, vector_size: int):
        collections = self.client.get_collections().collections
        names = {c.name for c in collections}

        if self.collection in names:
            return  # already exists

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

    def upsert(self, ids, vectors, payloads):
        points = [
            PointStruct(id=i, vector=v, payload=p)
            for i, v, p in zip(ids, vectors, payloads)
        ]
        self.client.upsert(
            collection_name=self.collection,
            points=points
        )

        count = self.client.count(self.collection, exact=True)
        print(f"[VectorStore] Stored vectors: {count.count}")

    def search(self, vector, limit=10):
        result = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=limit
        )
        return result.points

    def ensure_collection(self, vector_size: int):
        collections = self.client.get_collections().collections
        existing = {c.name for c in collections}
    
        if self.collection not in existing:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
   