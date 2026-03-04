from bytez import Bytez

from backend.config.settings import BYTEZ_API_KEY


sdk = Bytez(BYTEZ_API_KEY)

model = sdk.model("google/gemini-2.5-flash")


def rewrite_query(query):
    """
    Rewrite a user query to be more detailed and suitable for document retrieval.
    
    This helps improve retrieval quality by expanding short/vague queries into
    more comprehensive search queries that better match document content.
    
    Args:
        query: The original user query
    
    Returns:
        A rewritten, more detailed query
    """
    
    prompt = f"""Rewrite the following user query to be more detailed and specific for document retrieval.
Return ONLY the improved query, nothing else. No explanations or options.

Original Query:
{query}

Improved Query:"""

    results = model.run([{"role": "user", "content": prompt}])

    if results.error:
        raise Exception(f"Model error: {results.error}")

    # Handle bytez SDK response format
    output = results.output
    if isinstance(output, dict):
        if 'text' in output:
            rewritten_query = output['text'].strip()
        elif 'content' in output:
            rewritten_query = output['content'].strip()
        elif 'message' in output:
            rewritten_query = output['message'].strip()
        else:
            rewritten_query = str(output).strip()
    else:
        rewritten_query = str(output).strip()

    return rewritten_query
