from app.database.models.model_registry import ModelRegistry
from app.schemas.prompt_analysis import (
    PromptAnalysis,
    PromptCategory,
    PromptComplexity,
)
from app.schemas.selection_criteria import SelectionCriteria
from app.selector.model_selector import ModelSelector


def create_model(
    name: str,
    capabilities: list[str],
    quality: float,
    latency: float,
    input_cost: float,
    output_cost: float,
) -> ModelRegistry:

    model_ids = {
        "quality-model": 1,
        "fast-model": 2,
    }

    return ModelRegistry(
        id=model_ids[name],
        name=name,
        provider="test",
        capabilities=capabilities,
        context_window=128000,
        input_cost=input_cost,
        output_cost=output_cost,
        expected_quality=quality,
        expected_latency_ms=latency,
        is_active=True,
    )


def test_selector_prefers_quality():
    models = [
        create_model(
            name="quality-model",
            capabilities=["coding", "reasoning"],
            quality=0.95,
            latency=500,
            input_cost=0.01,
            output_cost=0.02,
        ),
        create_model(
            name="fast-model",
            capabilities=["coding"],
            quality=0.70,
            latency=100,
            input_cost=0.01,
            output_cost=0.02,
        ),
    ]

    analysis = PromptAnalysis(
        category=PromptCategory.CODING,
        complexity=PromptComplexity.HIGH,
        requires_reasoning=True,
        requires_tools=False,
        domain="software",
        confidence=0.95,
    )

    criteria = SelectionCriteria(
        capability_weight=0.10,
        quality_weight=0.60,
        reasoning_weight=0.20,
        latency_weight=0.05,
        cost_weight=0.05,
    )

    selector = ModelSelector()

    result = selector.select(
        analysis=analysis,
        models=models,
        criteria=criteria,
    )

    assert result.selected_model.name == "quality-model"


def test_selector_prefers_speed():
    models = [
        create_model(
            name="quality-model",
            capabilities=["coding", "reasoning"],
            quality=0.95,
            latency=500,
            input_cost=0.01,
            output_cost=0.02,
        ),
        create_model(
            name="fast-model",
            capabilities=["coding"],
            quality=0.70,
            latency=100,
            input_cost=0.01,
            output_cost=0.02,
        ),
    ]

    analysis = PromptAnalysis(
        category=PromptCategory.CODING,
        complexity=PromptComplexity.LOW,
        requires_reasoning=False,
        requires_tools=False,
        domain="software",
        confidence=0.95,
    )

    criteria = SelectionCriteria(
        capability_weight=0.10,
        quality_weight=0.10,
        reasoning_weight=0.00,
        latency_weight=0.75,
        cost_weight=0.05,
    )

    selector = ModelSelector()

    result = selector.select(
        analysis=analysis,
        models=models,
        criteria=criteria,
    )

    assert result.selected_model.name == "fast-model"