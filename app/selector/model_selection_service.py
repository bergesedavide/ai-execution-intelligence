from app.registry.model_service import ModelRegistryService
from app.schemas.model_selection import ModelSelection
from app.schemas.prompt_analysis import PromptAnalysis
from app.schemas.selection_criteria import SelectionCriteria
from app.selector.model_selector import ModelSelector


class ModelSelectionService:

    def __init__(
        self,
        model_registry_service: ModelRegistryService,
        model_selector: ModelSelector,
    ):
        self.model_registry_service = model_registry_service
        self.model_selector = model_selector

    def select_model(
        self,
        analysis: PromptAnalysis,
        criteria: SelectionCriteria,
    ) -> ModelSelection:

        models = self.model_registry_service.get_active_models()

        return self.model_selector.select(
            analysis=analysis,
            models=models,
            criteria=criteria,
        )