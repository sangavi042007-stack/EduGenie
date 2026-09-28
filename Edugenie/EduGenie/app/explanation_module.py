from app.config import get_settings
from app.gemini_client import generate_text


SYSTEM = """You are an expert teacher.
Explain difficult concepts in plain language for a beginner.
Use short sections, analogies, examples, and a brief recap.
Avoid unnecessary jargon."""


def _gemini_explanation(topic: str) -> str:
    prompt = f"""Explain this topic to a beginner:

{topic}

Structure:
1. Simple definition
2. How it works
3. One intuitive example
4. Key points to remember"""
    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        temperature=0.35,
        max_output_tokens=1000,
    )


def _local_explanation(topic: str) -> str:
    # Optional dependency path matching the project documentation's LaMini-Flan-T5 model.
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires the optional local AI dependencies. "
            "Run: pip install -r requirements-local.txt"
        ) from exc

    model_name = get_settings().local_explanation_model
    generator = pipeline(
        "text2text-generation",
        model=model_name,
        device=-1,
    )
    prompt = (
        "Explain the following topic simply for a beginner. "
        "Give a definition, how it works, an example, and key points: "
        f"{topic}"
    )
    result = generator(prompt, max_new_tokens=350, do_sample=False)
    return result[0]["generated_text"].strip()


async def explain_topic(topic: str) -> str:
    provider = get_settings().explanation_provider.lower()
    if provider == "local":
        return _local_explanation(topic)
    return _gemini_explanation(topic)
