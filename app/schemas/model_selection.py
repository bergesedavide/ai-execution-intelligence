from pydantic import BaseModel

from app.schemas.model import ModelInfo


class ModelScore(BaseModel):
    model_name: str
    score: float


class ModelSelection(BaseModel):
    selected_model: ModelInfo
    selected_model_id: int
    candidates: list[ModelScore]