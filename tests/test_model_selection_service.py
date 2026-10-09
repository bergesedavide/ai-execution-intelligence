from unittest.mock import Mock

from app.database.models.model_registry import ModelRegistry
from app.schemas.model_selection import ModelSelection
from app.schemas.prompt_analysis import (
    PromptAnalysis,
    PromptCategory,
    PromptComplexity,
)
from app.schemas.selection_criteria import SelectionCriteria
from app.selector.model_selection_service import ModelSelectionService


def test_model_selection_service():

    model_registry_service = Mock()
    model_selector = Mock()

    models = [
        ModelRegistry(
            id=1,
            name="test-model",
            provider="test",
            capabilities=["coding", "reasoning"],
            context_window=8192,
            input_cost=0.0,
            output_cost=0.0,
            expected_quality=0.80,
            expected_latency_ms=300.0,
            is_active=True,
        )
    ]

    model_registry_service.get_active_models.return_value = models

    expected_selection = ModelSelection(
        selected_model={
            "name": "test-model",
            "provider": "test",
            "capabilities": ["coding", "reasoning"],
            "context_window": 8192,
            "input_cost": 0.0,
            "output_cost": 0.0,
            "expected_quality": 0.80,
            "expected_latency_ms": 300.0,
        },
        selected_model_id=1,
        candidates=[
            {
                "model_name": "test-model",
                "score": 1.0,
            }
        ],
    )

    model_selector.select.return_value = expected_selection

    service = ModelSelectionService(
        model_registry_service=model_registry_service,
        model_selector=model_selector,
    )

    analysis = PromptAnalysis(
        category=PromptCategory.CODING,
        complexity=PromptComplexity.MEDIUM,
        requires_reasoning=True,
        requires_tools=False,
        domain="software",
        confidence=0.95,
    )

    criteria = SelectionCriteria(
        capability_weight=0.25,
        quality_weight=0.35,
        reasoning_weight=0.20,
        latency_weight=0.10,
        cost_weight=0.10,
    )

    result = service.select_model(
        analysis=analysis,
        criteria=criteria,
    )

    assert result == expected_selection

    model_registry_service.get_active_models.assert_called_once()

    model_selector.select.assert_called_once_with(
        analysis=analysis,
        models=models,
        criteria=criteria,
    )