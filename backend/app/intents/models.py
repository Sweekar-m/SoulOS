from pydantic import BaseModel, Field


class IntentResult(BaseModel):
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)
    entities: dict[str, str] = Field(default_factory=dict)
    requires_confirmation: bool = False


class IntentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
