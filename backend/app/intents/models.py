from pydantic import BaseModel, Field, field_validator


MAX_INTENT_TEXT_LENGTH = 2000


class IntentResult(BaseModel):
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)
    entities: dict[str, str] = Field(default_factory=dict)
    requires_confirmation: bool = False


class IntentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_INTENT_TEXT_LENGTH)

    @field_validator("text")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("text must contain non-whitespace characters")
        return normalized
