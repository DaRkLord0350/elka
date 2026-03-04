from backend.retrieval.hybrid_search import hybrid_search
from backend.llm.generator import generate_answer


def ask_question(question):

    chunks = hybrid_search(question)

    answer = generate_answer(question, chunks)

    return answer
