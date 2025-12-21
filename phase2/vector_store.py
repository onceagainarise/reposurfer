from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

class VectorStore:
    def __init__(self, collection_name: str):
        self.client = QdrantClient(":memory:")
        self.collection = collection_name

    def create(self, vector_size: int):
        self.client.recreate_collection(
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
        self.client.upsert(self.collection, points)
        count = self.client.count(self.collection, exact=True)
        print("Stored vectors:", count.count)

