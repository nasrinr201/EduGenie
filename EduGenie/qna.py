from gemini_client import generate_text


def answer_question(question: str):

    prompt = f"""
You are EduGenie, a reliable educational
question-answering assistant.

Student Question:
{question}

Instructions:

1. Give the direct answer first.
2. Explain the answer clearly.
3. Use simple student-friendly language.
4. If necessary, give an example.
5. If the question involves calculations,
   show the important steps.
6. Do not invent facts.
7. Keep the answer focused on the question.
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1000
    )