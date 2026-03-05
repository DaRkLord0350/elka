from backend.retrieval.vector_search import search
from backend.retrieval.bm25_search import keyword_search
from backend.retrieval.reranker import rerank


def hybrid_search(query, top_k=7):
    vector_results = search(query, top_k=10)
    keyword_results = keyword_search(query, top_k=10)
    
    seen = set()
    combined = []
    for chunk in vector_results + keyword_results:
        if chunk not in seen:
            seen.add(chunk)
            combined.append(chunk)
    
    if combined:
        reranked = rerank(query, combined, top_k=top_k)
        return reranked
    return combined[:top_k]
