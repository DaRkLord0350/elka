import faiss
import numpy as np
import pickle

from backend.config.settings import VECTOR_DB_PATH


def create_faiss_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, VECTOR_DB_PATH)

    return index