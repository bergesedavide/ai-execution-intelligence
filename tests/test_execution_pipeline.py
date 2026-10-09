from ollama import Client
from unittest.mock import Mock

from app.analyzer.prompt_analyzer import PromptAnalyzer
from app.database.engine import TestSessionLocal
from app.database.models.execution import Execution
from app.database.models.execution_event import ExecutionEvent
from app.execution.execution_pipeline import ExecutionPipeline
from app.execution.execution_service import ExecutionService
from app.registry.model_repository import ModelRepository
from app.registry.model_service import ModelRegistryService
from app.schemas.selection_criteria import SelectionCriteria
from app.selector.model_selection_service import ModelSelectionService
from app.selector.model_selector import ModelSelector
from app.tracking.event_repository import EventRepository
from app.tracking.event_tracker import EventTracker
from app.schemas.model import ModelInfo
from app.schemas.model_selection import ModelSelection, ModelScore
from app.schemas.prompt_analysis import (
    PromptAnalysis,
    PromptCategory,
    PromptComplexity,
)
from app.cost.cost_service import CostService
from app.evaluation.quality_evaluator import QualityEvaluator
from app.evaluation.quality_repository import QualityRepository
from app.schemas.quality_evaluation import QualityEvaluation


def test_execution_pipeline():

    client = Client(
        host="http://localhost:11435"
    )

    session = TestSessionLocal()

    analyzer = PromptAnalyzer(
        client=client,
        model="llama3.1:8b",
    )

    repository = ModelRepository(session)

    registry_service = ModelRegistryService(
        repository=repository,
    )

    selector = ModelSelector()

    model_selection_service = ModelSelectionService(
        model_registry_service=registry_service,
        model_selector=selector,
    )

    execution_service = ExecutionService(
        client=client,
        session=session,
    )

    cost_service = CostService()

    event_repository = EventRepository(session)

    event_tracker = EventTracker(
        repository=event_repository,
    )

    criteria = SelectionCriteria(
        capability_weight=1.0,
        quality_weight=1.0,
        reasoning_weight=1.0,
        latency_weight=1.0,
        cost_weight=1.0,
    )

    quality_evaluator = Mock()
    quality_evaluator.evaluate.return_value = QualityEvaluation(
        correctness=0.9,
        relevance=0.9,
        completeness=0.9,
        overall_score=0.9,
        reasoning="Test evaluation",
    )

    quality_repository = Mock()

    pipeline = ExecutionPipeline(
        analyzer=analyzer,
        model_selection_service=model_selection_service,
        execution_service=execution_service,
        event_tracker=event_tracker,
        cost_service=cost_service,
        quality_evaluator=quality_evaluator,
        quality_repository=quality_repository,
        criteria=criteria,
    )

    prompt = (
        "Explain what a Python decorator is in one sentence."
    )

    execution = None

    try:

        result = pipeline.run(prompt)

        assert result.response
        assert result.analysis is not None
        assert result.selection is not None

        assert result.selection.selected_model.name == (
            "llama3.1:8b"
        )

        execution = (
            session.query(Execution)
            .filter(Execution.prompt == prompt)
            .order_by(Execution.id.desc())
            .first()
        )

        assert execution is not None
        assert execution.id == result.execution_id
        assert execution.model_name == "llama3.1:8b"
        assert execution.status == "success"
        assert execution.latency_ms > 0
        assert execution.input_tokens is not None
        assert execution.output_tokens is not None

        assert result.cost is not None
        assert result.cost.input_cost >= 0.0
        assert result.cost.output_cost >= 0.0
        assert result.cost.total_cost == (
            result.cost.input_cost
            + result.cost.output_cost
        )

        events = (
            session.query(ExecutionEvent)
            .filter(
                ExecutionEvent.execution_id == execution.id
            )
            .order_by(ExecutionEvent.id)
            .all()
        )

        assert [event.event_type for event in events] == [
            "model_selected",
            "execution_started",
            "execution_completed",
        ]

    finally:

        if execution is not None:
            session.delete(execution)
            session.commit()

        session.close()

def test_execution_pipeline_failure():

    client = Mock()

    client.chat.side_effect = RuntimeError(
        "Simulated Ollama failure"
    )

    session = TestSessionLocal()

    analyzer = Mock()

    analyzer.analyze.return_value = PromptAnalysis(
        category=PromptCategory.CODING,
        complexity=PromptComplexity.LOW,
        requires_reasoning=False,
        requires_tools=False,
        domain="python",
        confidence=1.0,
    )

    selected_model = ModelInfo(
        name="llama3.1:8b",
        provider="ollama",
        capabilities=[
            "chat",
            "reasoning",
            "coding",
        ],
        context_window=8192,
        input_cost=0.0,
        output_cost=0.0,
        expected_quality=0.8,
        expected_latency_ms=1000,
    )

    model_selection_service = Mock()

    model_selection_service.select_model.return_value = (
        ModelSelection(
            selected_model=selected_model,
            selected_model_id=1,
            candidates=[
                ModelScore(
                    model_name="llama3.1:8b",
                    score=1.0,
                )
            ],
        )
    )

    execution_service = ExecutionService(
        client=client,
        session=session,
    )

    cost_service = CostService()

    event_repository = EventRepository(session)

    event_tracker = EventTracker(
        repository=event_repository,
    )

    criteria = SelectionCriteria(
        capability_weight=1.0,
        quality_weight=1.0,
        reasoning_weight=1.0,
        latency_weight=1.0,
        cost_weight=1.0,
    )

    quality_evaluator = Mock()
    quality_repository = Mock()

    pipeline = ExecutionPipeline(
        analyzer=analyzer,
        model_selection_service=model_selection_service,
        execution_service=execution_service,
        event_tracker=event_tracker,
        cost_service=cost_service,
        quality_evaluator=quality_evaluator,
        quality_repository=quality_repository,
        criteria=criteria,
    )

    prompt = "Test execution failure."

    execution = None

    try:

        try:
            pipeline.run(prompt)
            assert False, "Expected RuntimeError"

        except RuntimeError as error:
            assert str(error) == "Simulated Ollama failure"

        execution = (
            session.query(Execution)
            .filter(Execution.prompt == prompt)
            .order_by(Execution.id.desc())
            .first()
        )

        assert execution is not None
        assert execution.status == "error"

        events = (
            session.query(ExecutionEvent)
            .filter(
                ExecutionEvent.execution_id == execution.id
            )
            .order_by(ExecutionEvent.id)
            .all()
        )

        assert [event.event_type for event in events] == [
            "model_selected",
            "execution_started",
            "execution_failed",
        ]

    finally:

        if execution is not None:
            session.delete(execution)
            session.commit()

        session.close()

def test_execution_pipeline_quality_evaluation_failure():
    from types import SimpleNamespace
    from app.schemas.execution_cost import ExecutionCost

    analyzer = Mock()
    analyzer.analyze.return_value = PromptAnalysis(
        category=PromptCategory.CODING,
        complexity=PromptComplexity.LOW,
        requires_reasoning=False,
        requires_tools=False,
        domain="python",
        confidence=1.0,
    )

    selected_model = ModelInfo(
        name="llama3.1:8b",
        provider="ollama",
        capabilities=["chat", "reasoning", "coding"],
        context_window=8192,
        input_cost=0.0,
        output_cost=0.0,
        expected_quality=0.8,
        expected_latency_ms=1000,
    )

    model_selection_service = Mock()
    model_selection_service.select_model.return_value = ModelSelection(
        selected_model=selected_model,
        selected_model_id=1,
        candidates=[
            ModelScore(
                model_name="llama3.1:8b",
                score=1.0,
            )
        ],
    )

    execution = SimpleNamespace(
        id=123,
        input_cost=None,
        output_cost=None,
        total_cost=None,
    )

    execution_service = Mock()
    execution_service.create_execution.return_value = execution
    execution_service.execute.return_value = "Test response"

    cost_service = Mock()
    cost_service.calculate.return_value = ExecutionCost(
        input_cost=0.0,
        output_cost=0.0,
        total_cost=0.0,
    )

    event_tracker = Mock()

    quality_evaluator = Mock()
    quality_evaluator.evaluate.side_effect = RuntimeError(
        "Simulated quality evaluation failure"
    )

    quality_repository = Mock()

    pipeline = ExecutionPipeline(
        analyzer=analyzer,
        model_selection_service=model_selection_service,
        execution_service=execution_service,
        event_tracker=event_tracker,
        cost_service=cost_service,
        quality_evaluator=quality_evaluator,
        quality_repository=quality_repository,
        criteria=SelectionCriteria(
            capability_weight=1.0,
            quality_weight=1.0,
            reasoning_weight=1.0,
            latency_weight=1.0,
            cost_weight=1.0,
        ),
    )

    result = pipeline.run("Test quality evaluation failure.")

    assert result.response == "Test response"
    assert result.execution_id == 123
    assert result.quality is None

    execution_service.execute.assert_called_once_with(execution)
    execution_service.save.assert_called_once_with(execution)
    quality_repository.save.assert_not_called()

    event_types = [
        call.kwargs["event_type"]
        for call in event_tracker.track.call_args_list
    ]

    assert event_types == [
        "model_selected",
        "execution_started",
        "execution_completed",
        "quality_evaluation_failed",
    ]

    assert "execution_failed" not in event_types