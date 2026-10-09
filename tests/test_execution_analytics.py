from datetime import UTC, datetime

from app.analytics.execution_analytics_service import (
    ExecutionAnalyticsService,
)
from app.analytics.execution_repository import ExecutionRepository
from app.database.engine import TestSessionLocal
from app.database.models.execution import Execution
from app.database.models.model_registry import ModelRegistry


def test_execution_analytics_service():

    session = TestSessionLocal()

    model = (
        session.query(ModelRegistry)
        .filter_by(name="llama3.1:8b")
        .one()
    )

    executions = [
        Execution(
            prompt="Analytics test 1",
            model_id=model.id,
            model_name="analytics-test-model",
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
            latency_ms=100.0,
            input_tokens=10,
            output_tokens=20,
            status="success",
        ),
        Execution(
            prompt="Analytics test 2",
            model_id=model.id,
            model_name="analytics-test-model",
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
            latency_ms=200.0,
            input_tokens=20,
            output_tokens=40,
            status="success",
        ),
        Execution(
            prompt="Analytics test 3",
            model_id=model.id,
            model_name="analytics-test-model",
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
            latency_ms=300.0,
            input_tokens=30,
            output_tokens=60,
            status="error",
        ),
    ]

    try:

        session.add_all(executions)
        session.commit()

        repository = ExecutionRepository(session)

        service = ExecutionAnalyticsService(
            repository=repository,
        )

        metrics = service.get_metrics()

        assert metrics.total_executions >= 3
        assert metrics.successful_executions >= 2
        assert metrics.failed_executions >= 1

        assert 0.0 <= metrics.success_rate <= 1.0

        assert metrics.average_latency_ms is not None
        assert metrics.average_input_tokens is not None
        assert metrics.average_output_tokens is not None

    finally:

        for execution in executions:
            session.delete(execution)

        session.commit()
        session.close()