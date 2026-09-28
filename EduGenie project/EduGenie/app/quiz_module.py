import json
import re
from typing import List

from pydantic import BaseModel, Field

from app.gemini_client import generate_text


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]


def extract_json(text: str) -> dict:
    """
    Extract JSON even if Gemini wraps it in markdown code fences
    or adds a small amount of extra text.
    """

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    # First attempt: parse the entire response
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Second attempt: find the JSON object inside the response
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:
        json_text = text[start:end + 1]

        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Gemini did not return valid quiz JSON. "
        f"Response received: {text[:300]}"
    )


def validate_quiz(data: dict, question_count: int) -> dict:
    quiz = QuizResponse.model_validate(data)

    if len(quiz.questions) != question_count:
        raise ValueError(
            f"Expected {question_count} questions, "
            f"but received {len(quiz.questions)}."
        )

    for question in quiz.questions:
        if len(question.options) != 4:
            raise ValueError(
                "Every quiz question must contain exactly 4 options."
            )

        if question.correct_answer not in question.options:
            raise ValueError(
                "The correct answer must exactly match one of the options."
            )

    return quiz.model_dump()


async def generate_quiz(
    passage: str,
    question_count: int = 3
) -> dict:

    schema = {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string"
                        },
                        "options": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "minItems": 4,
                            "maxItems": 4
                        },
                        "correct_answer": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "question",
                        "options",
                        "correct_answer"
                    ]
                }
            }
        },
        "required": [
            "questions"
        ]
    }

    prompt = f"""
Create exactly {question_count} multiple-choice questions
from the educational material below.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do not use Markdown.
3. Do not write explanations outside the JSON.
4. Create exactly {question_count} questions.
5. Every question must have exactly 4 options.
6. Only one option must be correct.
7. The correct_answer must exactly match one option.
8. Questions must be based only on the supplied material.

Use this exact structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "correct_answer": "Option A"
        }}
    ]
}}

EDUCATIONAL MATERIAL:

{passage}
"""

    raw = generate_text(
        prompt,
        system_instruction=(
            "You are an educational quiz generator. "
            "Always produce valid JSON matching the requested structure."
        ),
        temperature=0.2,
        max_output_tokens=2500,
        response_mime_type="application/json",
        response_schema=schema,
    )

    try:
        data = extract_json(raw)
        return validate_quiz(data, question_count)

    except Exception as first_error:

        # Retry with an even simpler JSON instruction.
        retry_prompt = f"""
Generate exactly {question_count} MCQ questions from this material.

Return ONLY JSON.

Format:

{{
  "questions": [
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "..."
    }}
  ]
}}

Rules:
- Exactly {question_count} questions.
- Exactly four options per question.
- One correct answer.
- correct_answer must exactly equal one option.
- No Markdown.
- No explanation outside JSON.

Material:

{passage}
"""

        try:
            retry_raw = generate_text(
                retry_prompt,
                system_instruction=(
                    "Return only valid JSON. "
                    "Do not return Markdown or explanatory text."
                ),
                temperature=0.1,
                max_output_tokens=2500,
                response_mime_type="application/json",
            )

            retry_data = extract_json(retry_raw)
            return validate_quiz(
                retry_data,
                question_count
            )

        except Exception as retry_error:
            raise RuntimeError(
                "Quiz generation failed.\n"
                f"First attempt: {first_error}\n"
                f"Retry attempt: {retry_error}"
            ) from retry_error