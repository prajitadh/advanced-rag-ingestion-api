# embedding means numeric representation of the meaning of the sentence (vector representation)
from sentence_transformers import SentenceTransformer
from typing import List
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> List[float]:
    embedding = model.encode(text)
    return embedding.tolist()

def get_embeddings(texts: List[str]) -> List[List[float]]:
    # multiple chunks lai embed 
    embeddings = model.encode(texts)
    return embeddings.tolist()