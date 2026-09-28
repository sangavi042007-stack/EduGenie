import time
from functools import lru_cache

from google import genai
from google.genai import types

from app.config import get_settings


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache
def get_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. Add it to your .env file."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
    response_mime_type: str | None = None,
    response_schema=None,
) -> str:

    client = get_client()
    settings = get_settings()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
        response_mime_type=response_mime_type,
        response_schema=response_schema,
    )

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as error:

            error_text = str(error)

            # Retry temporary Gemini server errors
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

            # Other errors should immediately be reported
            raise RuntimeError(
                f"Gemini API request failed: {error}"
            ) from error

    raise RuntimeError(
        "Gemini API is temporarily unavailable after multiple retries."
    )