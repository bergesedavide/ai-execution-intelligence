from pydantic import BaseModel, Field


class QualityEvaluation(BaseModel):

    correctness: float = Field(
        ge=0.0,
        le=1.0,
    )

    relevance: float = Field(
        ge=0.0,
        le=1.0,
    )

    completeness: float = Field(
        ge=0.0,
        le=1.0,
    )

    overall_score: float = Field(
        ge=0.0,
        le=1.0,
    )

    reasoning: str