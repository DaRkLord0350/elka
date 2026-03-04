from backend.retrieval.vector_search import search
from backend.retrieval.bm25_search import keyword_search


def hybrid_search(query, top_k=5):

    vector_results = search(query, top_k)

    keyword_results = keyword_search(query, top_k)

    # Merge and deduplicate while preserving order
    seen = set()
    combined = []
    
    for chunk in vector_results + keyword_results:
        if chunk not in seen:
            seen.add(chunk)
            combined.append(chunk)
    
    return combined[:top_k]
