import faiss
import numpy as np
import pickle

from backend.ingestion.embeddings import generate_embeddings
from backend.config.settings import VECTOR_DB_PATH


def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, VECTOR_DB_PATH)
    return index


INDEX = None
CHUNKS = None


def _load_index_and_chunks():
    global INDEX, CHUNKS
    if INDEX is None:
        INDEX = faiss.read_index(VECTOR_DB_PATH)
    if CHUNKS is None:
        with open("vector_store/chunks.pkl", "rb") as f:
            CHUNKS = pickle.load(f)


def reload_index_and_chunks():
    """
    Force reload of the vector store and chunks.
    Call this after ingestion to refresh the cache.
    """
    global INDEX, CHUNKS
    INDEX = None
    CHUNKS = None
    _load_index_and_chunks()
    print("✓ Vector store reloaded")


def search(query, top_k=5):
    _load_index_and_chunks()
    query_embedding = generate_embeddings([query])
    query_embedding = np.array(query_embedding)
    distances, indices = INDEX.search(query_embedding, top_k)
    results = []
    for i in indices[0]:
        results.append(CHUNKS[i])
    return results
