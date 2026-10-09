from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    name: str
    provider: str
    capabilities: list[str]
    context_window: int = Field(gt=0)
    input_cost: float = Field(ge=0.0)
    output_cost: float = Field(ge=0.0)
    expected_quality: float = Field(ge=0.0, le=1.0)
    expected_latency_ms: float = Field(gt=0.0)