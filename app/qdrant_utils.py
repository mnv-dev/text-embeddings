import os
from typing import Optional, List

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.models import VectorParams

load_dotenv()

class QdrantConfig:
    def __init__(self):
        self.url = os.getenv("QDRANT_URL")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME")
        self.vector_size = int(os.getenv("QDRANT_VECTOR_SIZE"))
        self.distance_metric = os.getenv("QDRANT_DISTANCE_METRIC")

class QdrantVectorStore:
    def __init__(self, config: Optional[QdrantConfig] = None):
        self.config = config or QdrantConfig()
        self.client = QdrantClient(url=self.config.url)
        print("Connected to Qdrant Successfully!!")

    def create_collection(
            self,
            collection_name: Optional[str] = None,
            vector_size: Optional[int] = None,
            distance_metric: Optional[str] = None
            ) -> bool:
        name = collection_name or self.config.collection_name
        size = vector_size or self.config.vector_size
        dist_str = distance_metric or self.config.distance_metric

        try:
            existing_collections = self.client.get_collections().collections
            for coll in existing_collections:
                if coll.name == name:
                    print(f"Collection {name} already exists!!")
                    return True
            if not hasattr(models.Distance, dist_str):
                raise ValueError(f"Unsupported distance metric: {dist_str}")
            dist_enum = getattr(models.Distance, dist_str)

            self.client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=size,
                    distance=dist_enum
                )
            )
            print(f"Collection {name} created successfully!!")
            return True

        except Exception as e:
            print(f"Error creating collection: {str(e)}")
            raise e

    def insert_embeddings(
            self,
            texts: List[str],
            embeddings: List[List[float]],
            collection_name: Optional[str] = None,
            ) -> bool:

        name = collection_name or self.config.collection_name
        if len(texts) != len(embeddings):
            raise ValueError("Number of texts and embeddings must be equal!!")

        try:
            points = []
            for idx, (text, vector) in enumerate(zip(texts, embeddings)):
                points.append(models.PointStruct(
                    id=idx,
                    vector=vector,
                    payload={"text": text}
                ))

            self.client.upsert(
                collection_name=name,
                points=points
            )
            print(f"{len(points)} points inserted successfully!!")
            return True

        except Exception as e:
            print(f"Error inserting embeddings: {str(e)}")
            raise e

    def search_similar_texts(
            self,
            query_vector: List[float],
            top_k: int = 3,
            collection_name: Optional[str] = None
            ) -> List[dict]:
        name = collection_name or self.config.collection_name
        try:
            res = self.client.query_points(
                collection_name=name,
                query=query_vector,
                limit=top_k,
                with_payload=True,
                with_vectors=False,
            )
            hits = []
            for p in res.points:
                hits.append({
                    "id": p.id,
                    "text": (p.payload or {}).get("text"),
                    "score": p.score,
                })
            return hits
        except Exception as e:
            print(f"Error searching similar texts: {str(e)}")
            raise e

def initialize_collection() -> QdrantVectorStore:
    store = QdrantVectorStore()
    store.create_collection()
    return store