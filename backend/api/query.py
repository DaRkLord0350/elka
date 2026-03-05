from backend.retrieval.query_rewriter import rewrite_query
from backend.retrieval.hybrid_search import hybrid_search
from backend.llm.generator import generate_answer


def ask_question(question):
    print("\n" + "="*60)
    print("Original Query:", question)
    print("="*60)

    improved_query = rewrite_query(question)
    print("\nRewritten Query:", improved_query)
    print("="*60)

    chunks = hybrid_search(improved_query)
    print(f"\nRetrieved {len(chunks)} relevant chunks for context")
    print("="*60)

    answer = generate_answer(question, chunks)
    return answer
