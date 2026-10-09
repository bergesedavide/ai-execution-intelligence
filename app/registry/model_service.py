from app.database.models.model_registry import ModelRegistry
from app.registry.model_repository import ModelRepository
from app.schemas.model import ModelInfo


class ModelRegistryService:

    def __init__(self, repository: ModelRepository):
        self.repository = repository

    def register_model(self, model_info: ModelInfo) -> ModelRegistry:
        existing_model = self.repository.get_model(model_info.name)

        if existing_model is not None:
            raise ValueError(
                f"Model '{model_info.name}' is already registered."
            )

        return self.repository.add_model(model_info)

    def get_model(self, name: str) -> ModelRegistry | None:
        return self.repository.get_model(name)

    def get_all_models(self) -> list[ModelRegistry]:
        return self.repository.get_all_models()

    def get_active_models(self) -> list[ModelRegistry]:
        return self.repository.get_active_models()