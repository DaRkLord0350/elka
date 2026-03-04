from backend.ingestion.loader import load_documents
from backend.ingestion.preprocessing import clean_text
from backend.ingestion.chunking import chunk_text
from backend.ingestion.embeddings import generate_embeddings
from backend.retrieval.vector_search import create_faiss_index
from backend.config.settings import DOCUMENT_PATH

import numpy as np


print("Loading documents...")

docs = load_documents(DOCUMENT_PATH)

all_chunks = []

for doc in docs:

    text = clean_text(doc["text"])

    chunks = chunk_text(text)

    all_chunks.extend(chunks)


print("Generating embeddings...")

embeddings = generate_embeddings(all_chunks)

embeddings = np.array(embeddings)


print("Building FAISS index...")

create_faiss_index(embeddings)

print("Ingestion completed.")