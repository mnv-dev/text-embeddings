from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, status, Depends

from app.embeddings import EmbeddingGenerator
from app.qdrant_utils import QdrantVectorStore, initialize_collection
from dto.pydantic_utils import EmbedResponse, EmbedRequest

embedding_generator: Optional[EmbeddingGenerator] = None
vector_store: Optional[QdrantVectorStore] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global embedding_generator, vector_store
    print("🚀 Starting Embeddings API...")

    try:
        embedding_generator = EmbeddingGenerator()
        vector_store = initialize_collection()
        print("Embedding service and Qdrant connection initialized.")
    except Exception as e:
        print(f"Error during startup: {e}")

    yield

    print("Shutting down Embeddings API...")


# FastAPI app configuration
app = FastAPI(
    title="Embeddings API",
    description="REST API for generating and searching text embeddings using Google Vertex AI + Qdrant",
    version="1.0.0",
    lifespan=lifespan,
)

def get_embedding_generator() -> EmbeddingGenerator:
    if embedding_generator is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Embedding service not initialized"
        )
    return embedding_generator

def get_vector_store() -> QdrantVectorStore:
    if vector_store is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector store not initialized"
        )
    return vector_store


# API ENDPOINTS
@app.get("/")
async def root():
    return {"message": "Welcome to Embeddings API"}

@app.post("/embedding", response_model=EmbedResponse, status_code=200, tags=["Embeddings"])
async def generate_embedding(
    request: EmbedRequest,
    generator: EmbeddingGenerator = Depends(get_embedding_generator)
) -> EmbedResponse:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        embedding = generator.generate_embedding(request.text)
        return EmbedResponse(
            text=request.text,
            embedding=embedding,
            dimension=len(embedding)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating embedding: {str(e)}"
        ) from e

class SearchRequest(EmbedRequest):
    top_k: int = 5

@app.post("/search", status_code=200, tags=["Search"])
async def semantic_search(
    request: SearchRequest,
    generator: EmbeddingGenerator = Depends(get_embedding_generator),
    store: QdrantVectorStore = Depends(get_vector_store)
):
    text = (request.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty!!")

    try:
        query_vec = generator.generate_embedding(text)
        hits = store.search_similar_texts(query_vector=query_vec, top_k=request.top_k)
        return {
            "query": text,
            "top_k": request.top_k,
            "results": hits
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing search: {str(e)}"
        ) from e
