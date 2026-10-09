from datetime import UTC, datetime

from app.database.engine import SessionLocal
from app.database.models.execution import Execution
from app.database.models.model_registry import ModelRegistry
from app.database.models.quality_evaluation import (
    QualityEvaluation as QualityEvaluationModel,
)
from app.evaluation.quality_repository import QualityRepository
from app.schemas.quality_evaluation import (
    QualityEvaluation as QualityEvaluationSchema,
)


def test_quality_repository_save_and_get():
    session = SessionLocal()
    execution = None
    saved_evaluation = None

    try:
        model = (
            session.query(ModelRegistry)
            .filter_by(name="llama3.1:8b")
            .one()
        )

        execution = Execution(
            prompt="Test quality evaluation",
            model_id=model.id,
            model_name="test-quality-model",
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
            latency_ms=100.0,
            input_tokens=10,
            output_tokens=20,
            status="success",
        )

        session.add(execution)
        session.commit()
        session.refresh(execution)

        evaluation = QualityEvaluationSchema(
            correctness=0.9,
            relevance=0.8,
            completeness=0.7,
            overall_score=0.8,
            reasoning="The response is correct and relevant.",
        )

        repository = QualityRepository(session)

        saved_evaluation = repository.save(
            execution_id=execution.id,
            evaluation=evaluation,
        )

        assert saved_evaluation.id is not None
        assert saved_evaluation.execution_id == execution.id
        assert saved_evaluation.correctness == 0.9
        assert saved_evaluation.relevance == 0.8
        assert saved_evaluation.completeness == 0.7
        assert saved_evaluation.overall_score == 0.8
        assert saved_evaluation.reasoning == evaluation.reasoning

        retrieved = repository.get_by_execution_id(execution.id)

        assert retrieved is not None
        assert retrieved.id == saved_evaluation.id
        assert retrieved.execution_id == execution.id

    finally:
        if execution is not None:
            if saved_evaluation is not None:
                session.delete(saved_evaluation)

            session.delete(execution)
            session.commit()

        session.close()


def test_quality_repository_get_missing_evaluation():
    session = SessionLocal()

    try:
        repository = QualityRepository(session)

        result = repository.get_by_execution_id(-1)

        assert result is None

    finally:
        session.close()