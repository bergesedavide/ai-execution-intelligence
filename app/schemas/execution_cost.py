from pydantic import BaseModel, Field


class ExecutionCost(BaseModel):
    input_cost: float = Field(ge=0.0)
    output_cost: float = Field(ge=0.0)
    total_cost: float = Field(ge=0.0)