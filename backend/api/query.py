from backend.retrieval.vector_search import search
from backend.llm.generator import build_prompt


def ask_question(question):

    chunks = search(question)

    prompt = build_prompt(question, chunks)

    return prompt
