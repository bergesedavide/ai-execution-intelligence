from pydantic import BaseModel, Field


class ExecutionMetrics(BaseModel):

    total_executions: int = Field(ge=0)

    successful_executions: int = Field(ge=0)

    failed_executions: int = Field(ge=0)

    success_rate: float = Field(
        ge=0.0,
        le=1.0,
    )

    average_latency_ms: float | None = Field(
        default=None,
        ge=0.0,
    )

    average_input_tokens: float | None = Field(
        default=None,
        ge=0.0,
    )

    average_output_tokens: float | None = Field(
        default=None,
        ge=0.0,
    )