from ollama import Client

from app.analyzer.prompt_analyzer import PromptAnalyzer
from app.config import ANALYZER_MODEL, OLLAMA_HOST
from app.database.engine import SessionLocal
from app.execution.execution_pipeline import ExecutionPipeline
from app.execution.execution_service import ExecutionService
from app.registry.model_repository import ModelRepository
from app.registry.model_service import ModelRegistryService
from app.schemas.selection_criteria import SelectionCriteria
from app.selector.model_selection_service import ModelSelectionService
from app.selector.model_selector import ModelSelector
from app.cost.cost_service import CostService
from app.tracking.event_repository import EventRepository
from app.tracking.event_tracker import EventTracker
from app.evaluation.quality_evaluator import QualityEvaluator
from app.evaluation.quality_repository import QualityRepository


def main():
    ollama_client = Client(host=OLLAMA_HOST)
    session = SessionLocal()

    try:
        analyzer = PromptAnalyzer(
            client=ollama_client,
            model=ANALYZER_MODEL,
        )

        model_repository = ModelRepository(session)

        model_registry_service = ModelRegistryService(
            model_repository
        )

        model_selector = ModelSelector()

        model_selection_service = ModelSelectionService(
            model_registry_service=model_registry_service,
            model_selector=model_selector,
        )

        execution_service = ExecutionService(
            client=ollama_client,
            session=session,
        )

        event_repository = EventRepository(session)
        event_tracker = EventTracker(event_repository)

        cost_service = CostService()

        quality_evaluator = QualityEvaluator(
            client=ollama_client,
            model=ANALYZER_MODEL,
        )

        quality_repository = QualityRepository(session)

        criteria = SelectionCriteria(
            capability_weight=0.30,
            quality_weight=0.25,
            reasoning_weight=0.20,
            latency_weight=0.15,
            cost_weight=0.10,
        )

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

        prompt = input("\nEnter your prompt: ")

        result = pipeline.run(prompt)

        print("\nAI Execution Intelligence")
        print("-------------------------")

        print("\n[ANALYSIS]")
        print(f"Category: {result.analysis.category.value}")
        print(f"Complexity: {result.analysis.complexity.value}")
        print(
            f"Requires reasoning: "
            f"{result.analysis.requires_reasoning}"
        )
        print(
            f"Requires tools: "
            f"{result.analysis.requires_tools}"
        )
        print(f"Domain: {result.analysis.domain}")
        print(f"Confidence: {result.analysis.confidence:.2f}")

        print("\n[MODEL SELECTION]")
        print(
            f"Selected: "
            f"{result.selection.selected_model.name}"
        )

        print("\nCandidates:")
        for candidate in result.selection.candidates:
            print(
                f"- {candidate.model_name}: "
                f"{candidate.score:.4f}"
            )

        print("\n[EXECUTION]")
        print("\nResponse:")
        print(result.response)

        print(f"\nExecution ID: {result.execution_id}")

        print("\n[QUALITY EVALUATION]")

        if result.quality is None:
            print("Quality evaluation unavailable.")
        else:
            print(f"Correctness: {result.quality.correctness:.2f}/1.00")
            print(f"Relevance: {result.quality.relevance:.2f}/1.00")
            print(f"Completeness: {result.quality.completeness:.2f}/1.00")
            print(f"Overall score: {result.quality.overall_score:.2f}/1.00")
            print(f"Reasoning: {result.quality.reasoning}")

    finally:
        session.close()


if __name__ == "__main__":
    main()