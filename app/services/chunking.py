import re
from typing import List


def fixed_chunking(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

def recursive_chunking(text: str, max_chunk_size: int = 1000) -> List[str]:

    # Step 1: split by paragraphs
    paragraphs = text.split("\n\n")

    chunks = []

    for para in paragraphs:
        if len(para) <= max_chunk_size:
            chunks.append(para.strip())
        else:
            # Step 2: split by sentences
            sentences = re.split(r'(?<=[.!?]) +', para)

            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_chunk_size:
                    current_chunk += " " + sentence
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence

            if current_chunk:
                chunks.append(current_chunk.strip())

    return chunks

#this is the selector function.
def chunk_text(text: str, strategy: str = "fixed", **kwargs):
    #api should only call this function

    if strategy == "fixed":
        return fixed_chunking(
            text,
            chunk_size=kwargs.get("chunk_size", 1000),
            overlap=kwargs.get("overlap", 100)
        )

    elif strategy == "recursive":
        return recursive_chunking(
            text,
            max_chunk_size=kwargs.get("max_chunk_size", 1000)
        )

    else:
        raise ValueError("Invalid strategy: use 'fixed' or 'recursive'")