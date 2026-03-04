from bytez import Bytez

from backend.config.settings import BYTEZ_API_KEY
from backend.llm.prompt import PROMPT_TEMPLATE


sdk = Bytez(BYTEZ_API_KEY)

model = sdk.model("google/gemini-2.5-flash")


def build_prompt(question, chunks):

    context = "\n\n".join(chunks)

    prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    return prompt


def generate_answer(question, chunks):

    prompt = build_prompt(question, chunks)

    results = model.run([{"role": "user", "content": prompt}])

    if results.error:
        raise Exception(f"Model error: {results.error}")

    return results.output
