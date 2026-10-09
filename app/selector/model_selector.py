from app.database.models.model_registry import ModelRegistry
from app.schemas.model import ModelInfo
from app.schemas.model_selection import ModelScore, ModelSelection
from app.schemas.prompt_analysis import PromptAnalysis
from app.schemas.selection_criteria import SelectionCriteria
from app.selector.scoring import normalize_lower_is_better


class ModelSelector:

    def select(
        self,
        analysis: PromptAnalysis,
        models: list[ModelRegistry],
        criteria: SelectionCriteria,
    ) -> ModelSelection:

        latencies = [
            model.expected_latency_ms
            for model in models
        ]

        costs = [
            model.input_cost + model.output_cost
            for model in models
        ]

        min_latency = min(latencies)
        max_latency = max(latencies)

        min_cost = min(costs)
        max_cost = max(costs)

        scored_models = []

        for model in models:

            score = self._calculate_score(
                analysis=analysis,
                model=model,
                criteria=criteria,
                min_latency=min_latency,
                max_latency=max_latency,
                min_cost=min_cost,
                max_cost=max_cost,
            )

            scored_models.append(
                ModelScore(
                    model_name=model.name,
                    score=score,
                )
            )

        scored_models.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        selected_model = next(
            model
            for model in models
            if model.name == scored_models[0].model_name
        )

        model_info = ModelInfo(
            name=selected_model.name,
            provider=selected_model.provider,
            capabilities=selected_model.capabilities,
            context_window=selected_model.context_window,
            input_cost=selected_model.input_cost,
            output_cost=selected_model.output_cost,
            expected_quality=selected_model.expected_quality,
            expected_latency_ms=selected_model.expected_latency_ms,
        )

        return ModelSelection(
            selected_model=model_info,
            selected_model_id=selected_model.id,
            candidates=scored_models,
        )

    def _calculate_score(
        self,
        analysis: PromptAnalysis,
        model: ModelRegistry,
        criteria: SelectionCriteria,
        min_latency: float,
        max_latency: float,
        min_cost: float,
        max_cost: float,
    ) -> float:

        score = 0.0

        # Capability
        if analysis.category.value in model.capabilities:
            score += criteria.capability_weight

        # Quality
        score += (
            model.expected_quality
            * criteria.quality_weight
        )

        # Reasoning
        if analysis.requires_reasoning:
            if "reasoning" in model.capabilities:
                score += criteria.reasoning_weight

        # Latency
        latency_score = normalize_lower_is_better(
            value=model.expected_latency_ms,
            minimum=min_latency,
            maximum=max_latency,
        )

        score += (
            latency_score
            * criteria.latency_weight
        )

        # Cost
        model_cost = (
            model.input_cost
            + model.output_cost
        )

        cost_score = normalize_lower_is_better(
            value=model_cost,
            minimum=min_cost,
            maximum=max_cost,
        )

        score += (
            cost_score
            * criteria.cost_weight
        )

        return score