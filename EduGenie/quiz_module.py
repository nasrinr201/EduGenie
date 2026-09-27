import json
import re
from typing import Any

from gemini_client import generate_text


def clean_json_block(raw: str):
    cleaned = raw.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(r"\s*```$", "", cleaned)

    return cleaned.strip()


def validate_quiz(data: Any, count: int):

    if not isinstance(data, list):
        raise ValueError("Quiz response must be a JSON array.")

    if len(data) < count:
        raise ValueError(
            f"Expected {count} questions but received {len(data)}."
        )

    result = []

    for index, item in enumerate(data[:count], start=1):

        if not isinstance(item, dict):
            raise ValueError(f"Question {index} is invalid.")

        question = str(item.get("question", "")).strip()
        options = item.get("options")
        answer = str(item.get("answer", "")).strip()

        if (
            not question
            or not isinstance(options, list)
            or len(options) != 4
            or not answer
        ):
            raise ValueError(
                f"Question {index} has an invalid structure."
            )

        options = [str(option).strip() for option in options]

        if answer not in options:
            raise ValueError(
                f"Question {index}'s answer does not match an option."
            )

        result.append({
            "question": question,
            "options": options,
            "answer": answer
        })

    return result


def generate_quiz(passage: str, count: int = 3):

    count = max(1, min(count, 10))

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly {count} multiple-choice questions
from the following educational content.

CONTENT:
{passage}

Return ONLY valid JSON.

Use exactly this structure:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option"
  }}
]

Rules:

1. Exactly {count} questions.
2. Exactly four options for every question.
3. Only one correct answer.
4. Questions must be based on the content.
5. Distractors should be plausible.
6. The answer must exactly match one
   of the four options.
7. Do not use Markdown.
8. Do not add explanations outside JSON.
"""

    raw = generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1800
    )

    cleaned = clean_json_block(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON: {error}"
        )

    return validate_quiz(data, count)