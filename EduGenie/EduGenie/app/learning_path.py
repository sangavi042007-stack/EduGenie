from app.gemini_client import generate_text


SYSTEM = """You are an educational curriculum planner.
Create practical learning paths that progress from beginner to advanced.
Be realistic about prerequisites and study time.
Resource suggestions must be clearly labeled as suggestions; do not invent exact URLs."""


async def get_learning_recommendations(topic: str) -> str:
    prompt = f"""Create a personalized learning path for:

{topic}

Include:
1. Prerequisites
2. Beginner stage
3. Intermediate stage
4. Advanced stage
5. Suggested weekly timeline
6. Practice projects or exercises
7. Types of resources to use (videos, articles, books, documentation)
8. A short self-check after each stage"""
    return generate_text(
        prompt,
        system_instruction=SYSTEM,
        temperature=0.45,
        max_output_tokens=1800,
    )
