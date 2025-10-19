import types
import pytest

from app.qdrant_utils import QdrantVectorStore, QdrantConfig

class DummyCollectionsResponse:
    def __init__(self, names):
        self.collections = [types.SimpleNamespace(name=n) for n in names]

class DummyQueryResultPoint:
    def __init__(self, pid, text, score):
        self.id = pid
        self.payload = {"text": text}
        self.score = score

class DummyQueryResult:
    def __init__(self, points):
        self.points = points

class FakeQdrantClient:
    def __init__(self):
        self.created = {}
        self.upserts = {}
        self.query_calls = []

    def get_collections(self):
        return DummyCollectionsResponse(list(self.created.keys()))

    def create_collection(self, collection_name, vectors_config):
        self.created[collection_name] = {
            "size": vectors_config.size,
            "distance": vectors_config.distance
        }

    def upsert(self, collection_name, points):
        self.upserts.setdefault(collection_name, [])
        self.upserts[collection_name].extend(points)

    def query_points(self, collection_name, query, limit, with_payload, with_vectors):
        self.query_calls.append(
            {"collection": collection_name, "query": query, "limit": limit}
        )
        pts = []
        for i in range(limit):
            pts.append(DummyQueryResultPoint(pid=i, text=f"text-{i}", score=1.0 - 0.01 * i))
        return DummyQueryResult(pts)

@pytest.fixture
def store(monkeypatch):
    cfg = QdrantConfig()
    cfg.url = "http://fake"
    cfg.collection_name = "test_col"
    cfg.vector_size = 3
    cfg.distance_metric = "COSINE"

    fake_client = FakeQdrantClient()

    def fake_init(self, config=None):
        self.config = config or cfg
        self.client = fake_client
        print("Connected to Qdrant Successfully!!")

    monkeypatch.setattr(QdrantVectorStore, "__init__", fake_init)
    return QdrantVectorStore(cfg)

def test_create_collection_creates_when_missing(store):
    ok = store.create_collection(collection_name="new_col", vector_size=8, distance_metric="DOT")
    assert ok is True

def test_create_collection_returns_true_when_exists(store):
    assert store.create_collection(collection_name="exists", vector_size=4, distance_metric="COSINE")
    assert store.create_collection(collection_name="exists", vector_size=4, distance_metric="COSINE")

def test_insert_and_query_roundtrip_shapes(store):
    coll = "rt_col"
    assert store.create_collection(collection_name=coll, vector_size=3, distance_metric="COSINE")

    texts = ["a", "b", "c"]
    vectors = [
        [0.1, 0.2, 0.3],
        [0.0, -0.5, 0.9],
        [1.0, 0.0, 0.0],
    ]
    assert store.insert_embeddings(texts=texts, embeddings=vectors, collection_name=coll) is True

    results = store.search_similar_texts(query_vector=[0.1, 0.2, 0.3], top_k=2, collection_name=coll)
    assert isinstance(results, list)
    assert len(results) == 2
    assert set(results[0].keys()) == {"id", "text", "score"}