from datetime import UTC, datetime

from app.analytics.execution_repository import ExecutionRepository
from app.database.engine import SessionLocal
from app.database.models.execution import Execution
from app.database.models.model_registry import ModelRegistry


def test_execution_repository():

    session = SessionLocal()

    model = (
        session.query(ModelRegistry)
        .filter_by(name="llama3.1:8b")
        .one()
    )

    executions = [
        Execution(
            prompt="Test prompt 1",
            model_id=model.id,
            model_name="test-model-a",
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
            latency_ms=100.0,
            input_tokens=10,
            output_tokens=20,
            status="success",
        ),
        Execution(
            prompt="Test prompt 2",
            model_id=model.id,
            model_name="test-model-a",
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
            latency_ms=200.0,
            input_tokens=20,
            output_tokens=30,
            status="success",
        ),
        Execution(
            prompt="Test prompt 3",
            model_id=model.id,
            model_name="test-model-b",
            started_at=datetime.now(UTC),
            completed_at=datetime.now(UTC),
            latency_ms=300.0,
            input_tokens=30,
            output_tokens=40,
            status="error",
        ),
    ]

    try:

        session.add_all(executions)
        session.commit()

        for execution in executions:
            session.refresh(execution)

        repository = ExecutionRepository(session)

        # get_execution
        result = repository.get_execution(
            executions[0].id
        )

        assert result is not None
        assert result.id == executions[0].id

        # get_recent_executions
        recent = repository.get_recent_executions(
            limit=3
        )

        assert len(recent) >= 3

        # get_executions_by_model
        model_executions = (
            repository.get_executions_by_model(
                "test-model-a"
            )
        )

        expected_ids = {
            executions[0].id,
            executions[1].id,
        }

        actual_ids = {
            execution.id
            for execution in model_executions
        }

        assert expected_ids.issubset(actual_ids)

        # get_successful_executions
        successful = (
            repository.get_successful_executions()
        )

        successful_ids = {
            execution.id
            for execution in successful
        }

        assert executions[0].id in successful_ids
        assert executions[1].id in successful_ids
        assert executions[2].id not in successful_ids

    finally:

        for execution in executions:
            session.delete(execution)

        session.commit()
        session.close()