import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

VECTOR_DB_PATH = "vector_store/faiss_index"
DOCUMENT_PATH = "data/documents"

BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")