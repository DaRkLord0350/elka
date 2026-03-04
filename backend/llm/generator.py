from backend.llm.prompt import PROMPT_TEMPLATE


def build_prompt(question, chunks):

    context = "\n\n".join(chunks)

    prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    return prompt
