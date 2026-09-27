from gemini_client import generate_text


def summarize_text(text: str):

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational passage.

PASSAGE:
{text}

Instructions:

1. Keep the main ideas.
2. Remove unnecessary repetition.
3. Use simple language.
4. Use bullet points where useful.
5. Make it useful for quick revision.
6. Do not add information that is not present
   in the original passage.
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1000
    )