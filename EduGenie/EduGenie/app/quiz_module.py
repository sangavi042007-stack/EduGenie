from typing import List
from pydantic import BaseModel, Field

from app.gemini_client import generate_text


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]


def _validate_quiz(data: dict, count: int) -> QuizResponse:
    quiz = QuizResponse.model_validate(data)
    if len(quiz.questions) != count:
        raise ValueError(f"Model returned {len(quiz.questions)} questions; expected {count}.")
    for item in quiz.questions:
        if item.correct_answer not in item.options:
            raise ValueError("A correct_answer must exactly match one of the options.")
    return quiz


async def generate_quiz(passage: str, question_count: int = 3) -> dict:
    schema = {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 4,
                            "maxItems": 4,
                        },
                        "correct_answer": {"type": "string"},
                    },
                    "required": ["question", "options", "correct_answer"],
                },
            }
        },
        "required": ["questions"],
    }

    prompt = f"""Create exactly {question_count} multiple-choice questions from the passage below.

Rules:
- Questions must be answerable from the passage.
- Each question has exactly four options.
- Exactly one option is correct.
- Keep distractors plausible but clearly incorrect.
- Return only the requested JSON structure.

PASSAGE:
{passage}"""

    raw = generate_text(
        prompt,
        system_instruction="You generate reliable educational assessments.",
        temperature=0.2,
        max_output_tokens=1800,
        response_mime_type="application/json",
        response_schema=schema,
    )

    try:
        import json
        data = json.loads(raw)
        return _validate_quiz(data, question_count).model_dump()
    except Exception as exc:
        raise RuntimeError(f"Quiz generation/parsing failed: {exc}") from exc
