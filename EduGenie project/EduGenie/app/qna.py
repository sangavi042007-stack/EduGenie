from app.gemini_client import generate_text

SYSTEM = """You are EduGenie, a careful educational assistant.
Answer academic questions accurately and clearly.
Use simple language appropriate for a learner.
If a question is ambiguous, state the assumption you are making.
Do not invent sources, facts, citations, or numerical results."""


async def answer_question(question: str) -> str:
    prompt = f"""Answer the student's question.

Question:
{question}

Give a concise answer first, then a short explanation or example when useful."""
    return generate_text(prompt, system_instruction=SYSTEM, temperature=0.3)
