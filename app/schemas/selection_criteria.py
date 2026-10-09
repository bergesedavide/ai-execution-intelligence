from pydantic import BaseModel, Field


class SelectionCriteria(BaseModel):
    capability_weight: float = Field(ge=0.0, le=1.0)
    quality_weight: float = Field(ge=0.0, le=1.0)
    reasoning_weight: float = Field(ge=0.0, le=1.0)
    latency_weight: float = Field(ge=0.0, le=1.0)
    cost_weight: float = Field(ge=0.0, le=1.0)