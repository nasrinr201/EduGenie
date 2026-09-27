from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner"):

    prompt = f"""
You are EduGenie, a personalized learning assistant.

Create a structured learning path for:

Topic:
{topic}

Student Level:
{level}

Include:

1. Learning goal
2. Beginner concepts
3. Intermediate concepts
4. Advanced concepts
5. Suggested timeline
6. Practice activities
7. Recommended resource types
8. Final project or practice idea

Instructions:

- Start from basics.
- Progress gradually.
- Use simple student-friendly language.
- Make the plan practical.
- Explain why each stage is useful.
- Do not invent URLs.
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=1600
    )