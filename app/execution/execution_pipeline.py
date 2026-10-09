from app.schemas.model_selection import ModelSelection
from app.schemas.prompt_analysis import PromptAnalysis
from app.schemas.selection_criteria import SelectionCriteria
from app.schemas.execution_result import ExecutionResult

from app.execution.execution_service import ExecutionService
from app.selector.model_selection_service import ModelSelectionService
from app.analyzer.prompt_analyzer import PromptAnalyzer

from app.tracking.event_tracker import EventTracker
from app.cost.cost_service import CostService

from app.evaluation.quality_evaluator import QualityEvaluator
from app.evaluation.quality_repository import QualityRepository


class ExecutionPipeline:

    def __init__(
        self,
        analyzer: PromptAnalyzer,
        model_selection_service: ModelSelectionService,
        execution_service: ExecutionService,
        event_tracker: EventTracker,
        cost_service: CostService,
        quality_evaluator: QualityEvaluator,
        quality_repository: QualityRepository,
        criteria: SelectionCriteria,
    ):
        self.analyzer = analyzer
        self.model_selection_service = model_selection_service
        self.execution_service = execution_service
        self.event_tracker = event_tracker
        self.cost_service = cost_service
        self.quality_evaluator = quality_evaluator
        self.quality_repository = quality_repository
        self.criteria = criteria

    def run(self, prompt: str) -> ExecutionResult:
        analysis: PromptAnalysis = self.analyzer.analyze(prompt)

        selection: ModelSelection = self.model_selection_service.select_model(
            analysis=analysis,
            criteria=self.criteria,
        )

        selected_model = selection.selected_model

        execution = self.execution_service.create_execution(
            prompt=prompt,
            model_id=selection.selected_model_id,
            model_name=selected_model.name,
        )

        self.event_tracker.track(
            execution_id=execution.id,
            event_type="model_selected",
        )

        self.event_tracker.track(
            execution_id=execution.id,
            event_type="execution_started",
        )

        # Phase 1: execute the model and calculate costs
        try:
            response = self.execution_service.execute(execution)

            cost = self.cost_service.calculate(
                execution=execution,
                model=selected_model,
            )

            execution.input_cost = cost.input_cost
            execution.output_cost = cost.output_cost
            execution.total_cost = cost.total_cost

            self.execution_service.save(execution)

        except Exception:
            self.event_tracker.track(
                execution_id=execution.id,
                event_type="execution_failed",
            )
            raise

        self.event_tracker.track(
            execution_id=execution.id,
            event_type="execution_completed",
        )

        # Phase 2: evaluate the response independently
        quality = None

        try:
            quality = self.quality_evaluator.evaluate(
                prompt=prompt,
                response=response,
            )

            self.quality_repository.save(
                execution_id=execution.id,
                evaluation=quality,
            )

        except Exception:
            self.event_tracker.track(
                execution_id=execution.id,
                event_type="quality_evaluation_failed",
            )

        return ExecutionResult(
            response=response,
            analysis=analysis,
            selection=selection,
            execution_id=execution.id,
            cost=cost,
            quality=quality,
        )