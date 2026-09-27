import os
import time
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

DEFAULT_MODEL = "gemini-3.8-flash"


@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=api_key)


def generate_text(
    prompt: str,
    temperature: float = 0.4,
    max_output_tokens: int = 1200
):
    model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    client = get_client()

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens
                )
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text.strip()

        except Exception as error:
            last_error = error

            if "503" not in str(error) and "UNAVAILABLE" not in str(error):
                raise

            if attempt < 2:
                time.sleep(3)

    raise RuntimeError(
        "Gemini is temporarily busy. Please try again in a few seconds."
    ) from last_error