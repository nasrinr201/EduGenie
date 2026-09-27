from gemini_client import generate_text


def explain_topic(topic: str):

    prompt = f"""
You are EduGenie, an educational AI assistant.

Explain the following topic to a student who
does not have much prior knowledge.

Topic:
{topic}

Instructions:

1. Give a simple one-sentence definition.
2. Explain the topic using simple language.
3. Give 3 to 5 important points.
4. Give one simple example.
5. Avoid unnecessary technical words.
6. Keep the explanation concise.
7. Make the explanation suitable for exam preparation.
"""

    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=900
    )