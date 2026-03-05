from rank_bm25 import BM25Okapi
import pickle

BM25 = None
CHUNKS = None


def _load_bm25_and_chunks():
    global BM25, CHUNKS
    if BM25 is None:
        with open("vector_store/chunks.pkl", "rb") as f:
            CHUNKS = pickle.load(f)
        tokenized_chunks = [chunk.split() for chunk in CHUNKS]
        BM25 = BM25Okapi(tokenized_chunks)


def keyword_search(query, top_k=5):
    _load_bm25_and_chunks()
    tokenized_query = query.split()
    scores = BM25.get_scores(tokenized_query)
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    results = []
    for i in ranked_indices[:top_k]:
        results.append(CHUNKS[i])
    return results
