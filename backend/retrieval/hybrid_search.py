from backend.retrieval.vector_search import search
from backend.retrieval.bm25_search import keyword_search
from backend.retrieval.reranker import rerank


def hybrid_search(query, top_k=5):
    """
    Hybrid search combining vector search, BM25, and reranking.
    
    Pipeline:
    1. Vector search (semantic) - top 10
    2. BM25 search (keyword) - top 10
    3. Merge and deduplicate - combined pool
    4. Rerank using cross-encoder - top 5
    
    Args:
        query: The search query
        top_k: Number of final chunks to return
    
    Returns:
        List of top-k reranked chunks
    """
    
    # Retrieve candidates from both methods
    vector_results = search(query, top_k=10)
    keyword_results = keyword_search(query, top_k=10)
    
    # Merge and deduplicate
    seen = set()
    combined = []
    
    for chunk in vector_results + keyword_results:
        if chunk not in seen:
            seen.add(chunk)
            combined.append(chunk)
    
    # Rerank using cross-encoder model
    if combined:
        reranked = rerank(query, combined, top_k=top_k)
        return reranked
    
    return combined[:top_k]
