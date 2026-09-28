from app.gemini_client import generate_text


SYSTEM = """You summarize educational material faithfully.
Preserve important facts, definitions, relationships, and conclusions.
Remove repetition and unnecessary wording.
Never add information that is not supported by the supplied text."""


async def summarize_text(text: str) -> str:
    prompt = f"""Summarize the following educational passage.

Return:
- A short overview
- 3 to 7 key points
- Important terms or formulas, if present

PASSAGE:
{text}"""
    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        temperature=0.2,
        max_output_tokens=1200,
    )
