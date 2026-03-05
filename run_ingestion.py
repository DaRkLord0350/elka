from backend.ingestion.loader import load_documents
from backend.ingestion.preprocessing import clean_text
from backend.ingestion.chunking import chunk_text
from backend.ingestion.embeddings import generate_embeddings
from backend.retrieval.vector_search import create_faiss_index
from backend.config.settings import DOCUMENT_PATH

import numpy as np
import pickle
import os

print("="*60)
print("STARTING INGESTION PIPELINE")
print("="*60)

# Check if documents exist
if not os.path.exists(DOCUMENT_PATH):
    print(f"WARNING: Document path not found: {DOCUMENT_PATH}")
    print("Creating directory...")
    os.makedirs(DOCUMENT_PATH, exist_ok=True)

print(f"\n Looking for documents in: {DOCUMENT_PATH}")
print("Loading documents...")
docs = load_documents(DOCUMENT_PATH)
print(f" Loaded {len(docs)} documents")

if len(docs) == 0:
    print(" No documents found. Skipping ingestion.")
    print("Make sure you have synced data first!")
    exit(0)

print("\n Chunking documents...")
all_chunks = []
for doc_idx, doc in enumerate(docs, 1):
    text = clean_text(doc["text"])
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "text": chunk,
            "source": doc["source"],
            "chunk_id": i
        })
    print(f"   Document {doc_idx}: {len(chunks)} chunks from {doc['source']}")

print(f" Total chunks created: {len(all_chunks)}")

if len(all_chunks) == 0:
    print(" No chunks created. Documents may be empty.")
    exit(0)

print("\n Generating embeddings...")
embeddings = generate_embeddings([c["text"] for c in all_chunks])
embeddings = np.array(embeddings)
print(f" Generated {len(embeddings)} embeddings")
print(f"  Embedding dimension: {embeddings.shape[1]}")

print("\n Building FAISS index...")
create_faiss_index(embeddings)
print(f" FAISS index created")

print("\n Saving chunks metadata...")
os.makedirs("vector_store", exist_ok=True)
with open("vector_store/chunks.pkl", "wb") as f:
    pickle.dump(all_chunks, f)
print(f" Saved {len(all_chunks)} chunks metadata")

print("\n" + "="*60)
print(" INGESTION COMPLETED SUCCESSFULLY")
print("="*60)
print(f"\nSummary:")
print(f"  Documents processed: {len(docs)}")
print(f"  Total chunks: {len(all_chunks)}")
print(f"  Vector dimension: {embeddings.shape[1]}")
print(f"  Index size: {embeddings.nbytes / 1024 / 1024:.2f} MB")
print("\nYour documents are now searchable! ")
