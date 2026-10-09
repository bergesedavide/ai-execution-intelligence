from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.model_registry import ModelRegistry
from app.schemas.model import ModelInfo


class ModelRepository:

    def __init__(self, session: Session):
        self.session = session

    def add_model(self, model_info: ModelInfo) -> ModelRegistry:

        model = ModelRegistry(
            name=model_info.name,
            provider=model_info.provider,
            capabilities=model_info.capabilities,
            context_window=model_info.context_window,
            input_cost=model_info.input_cost,
            output_cost=model_info.output_cost,
            expected_quality=model_info.expected_quality,
            expected_latency_ms=model_info.expected_latency_ms,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        return model

    def get_model(self, name: str) -> ModelRegistry | None:

        statement = select(ModelRegistry).where(
            ModelRegistry.name == name
        )

        return self.session.execute(statement).scalar_one_or_none()

    def get_all_models(self) -> list[ModelRegistry]:

        statement = select(ModelRegistry)

        return list(
            self.session.execute(statement).scalars().all()
        )

    def get_active_models(self) -> list[ModelRegistry]:

        statement = select(ModelRegistry).where(
            ModelRegistry.is_active.is_(True)
        )

        return list(
            self.session.execute(statement).scalars().all()
        )