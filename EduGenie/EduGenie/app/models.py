from pydantic import BaseModel, Field, field_validator

from app.config import get_settings


def _validate_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Input text cannot be empty.")
    limit = get_settings().max_input_chars
    if len(value) > limit:
        raise ValueError(f"Input is too long. Maximum length is {limit} characters.")
    return value


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Topic, question, or passage")

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _validate_text(value)


class QuizRequest(TextRequest):
    question_count: int = Field(default=3, ge=1, le=10)
