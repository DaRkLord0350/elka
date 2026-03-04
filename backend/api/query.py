from backend.retrieval.vector_search import search
from backend.llm.generator import generate_answer


def ask_question(question):

    chunks = search(question)

    answer = generate_answer(question, chunks)

    return answer
