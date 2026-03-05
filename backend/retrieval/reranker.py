from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-base")


def rerank(query, chunks, top_k=5):
    if not chunks:
        return []
    pairs = [(query, chunk["text"]) for chunk in chunks]
    scores = reranker.predict(pairs)
    scored_chunks = list(zip(chunks, scores))
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    reranked_chunks = [chunk for chunk, score in scored_chunks[:top_k]]
    return reranked_chunks
