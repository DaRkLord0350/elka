from bytez import Bytez
from backend.config.settings import BYTEZ_API_KEY
from backend.llm.prompt import PROMPT_TEMPLATE

sdk = Bytez(BYTEZ_API_KEY)
model = sdk.model("google/gemini-2.5-flash")


def build_prompt(question, chunks):
    context = "\n\n".join([chunk["text"] for chunk in chunks])
    return PROMPT_TEMPLATE.format(context=context, question=question)


def generate_answer(question, chunks):
    prompt = build_prompt(question, chunks)
    results = model.run([{"role": "user", "content": prompt}])
    if results.error:
        raise Exception(f"Model error: {results.error}")
    output = results.output
    if isinstance(output, dict):
        if 'content' in output:
            return output['content']
        elif 'text' in output:
            return output['text']
        elif 'message' in output:
            return output['message']
        else:
            return str(output)
    return output
