from pydantic import BaseModel

from app.schemas.execution_cost import ExecutionCost
from app.schemas.model_selection import ModelSelection
from app.schemas.prompt_analysis import PromptAnalysis
from app.schemas.quality_evaluation import QualityEvaluation


class ExecutionResult(BaseModel):
    response: str
    analysis: PromptAnalysis
    selection: ModelSelection
    execution_id: int
    cost: ExecutionCost
    quality: QualityEvaluation | None = None