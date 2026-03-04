from sentence_transformers import CrossEncoder

# Load reranker model
reranker = CrossEncoder("BAAI/bge-reranker-base")


def rerank(query, chunks, top_k=5):
    """
    Rerank chunks based on relevance to query using a cross-encoder model.
    
    Args:
        query: The search query
        chunks: List of retrieved chunks
        top_k: Number of top chunks to return
    
    Returns:
        List of reranked chunks (top_k most relevant)
    """
    
    if not chunks:
        return []
    
    # Create (query, chunk) pairs
    pairs = []
    for chunk in chunks:
        pairs.append((query, chunk))
    
    # Get relevance scores
    scores = reranker.predict(pairs)
    
    # Combine chunks with scores
    scored_chunks = list(zip(chunks, scores))
    
    # Sort by relevance score (descending)
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    
    # Extract top-k chunks
    reranked_chunks = [chunk for chunk, score in scored_chunks[:top_k]]
    
    return reranked_chunks
