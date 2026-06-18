from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import uuid
from app.config import settings
from app.services.embeddings import get_embeddings
from app.vectorstore.qdrant_client import upsert_chunks

client = QdrantClient(url=settings.QDRANT_URL)

def create_collection():
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if settings.QDRANT_COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,  # MiniLM embedding size
                distance=Distance.COSINE
            )
        )

def upsert_chunks(chunks: list[str], embeddings: list[list[float]], document_id: int):
    points = []

    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append(
            {
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": {
                    "text": chunk,
                    "document_id": document_id,
                    "chunk_index": i
                }
            }
        )

    client.upsert(
        collection_name=settings.QDRANT_COLLECTION_NAME,
        points=points
    )

def embed_and_store(chunks: list[str], document_id: int):
    embeddings = get_embeddings(chunks)
    upsert_chunks(chunks, embeddings, document_id)