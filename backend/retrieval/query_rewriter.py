from bytez import Bytez
from backend.config.settings import BYTEZ_API_KEY

sdk = Bytez(BYTEZ_API_KEY)
model = sdk.model("google/gemini-2.5-flash")


def rewrite_query(query):
    prompt = f"""Rewrite the following user query to be more detailed and specific for document retrieval.
Return ONLY the improved query, nothing else. No explanations or options.

Original Query:
{query}

Improved Query:"""

    results = model.run([{"role": "user", "content": prompt}])
    if results.error:
        raise Exception(f"Model error: {results.error}")

    output = results.output
    if isinstance(output, dict):
        if 'text' in output:
            return output['text'].strip()
        elif 'content' in output:
            return output['content'].strip()
        elif 'message' in output:
            return output['message'].strip()
        else:
            return str(output).strip()
    return str(output).strip()
